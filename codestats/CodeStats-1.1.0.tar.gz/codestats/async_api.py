import asyncio

import aiohttp

from codestats.bases import User as _User


class User(_User):
    def __init__(self, name: str, auto_load: bool=True, loop: asyncio.AbstractEventLoop=None):
        """
        Creates a user instances and optionally loads the user's data from the API. This can
         be disabled by setting the the ``auto_load``

        :param name: The name of the user. This should be the name as it's known at the API
        :param auto_load: Load the user's data from the API after initialization. If set to ``False``
            the ``load`` method should be awaited manually.
        :param loop: The event loop to be used. Defaults to the result of ``asyncio.get_event_loop``
        """
        self.name = name
        self._loop = loop
        self.session = aiohttp.ClientSession(loop=self.loop)

        if auto_load:
            self.loop.call_soon_threadsafe(self.load())

    async def load(self):
        if self.name is None or self.name == "":
            raise ValueError("Username cannot be {}".format(self.name))

        url = self.URL + self.name
        response: aiohttp.ClientResponse = await self.session.get(url)
        body = await response.json()
        self._parse(body)

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        if self._loop is None:
            self._loop = asyncio.get_event_loop()

        return self._loop

    def __del__(self):
        """
        Hacky way to make sure the AioHTTP session get's closed when the object is
         destroyed. Using the class as a context manager is recommended.
        """
        self.session.close()

    async def __aenter__(self):
        """
        Enables the class to be used as a context manager

        Eg:
        >>> async with User("niekkeijzer", False) as user:
        >>>     print(user.languages)
        :return:
        """
        self.session = aiohttp.ClientSession(loop=self.loop)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
