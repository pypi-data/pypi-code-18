import asyncio

from .api import HTTPClient
from .category import Category
from .channel import Channel, OnlineChannel


class Client:
    def __init__(self, *, token=None, loop=None, **options):
        self._loop = asyncio.get_event_loop() if loop is None else loop
        self._listeners = {}

        connector = options.get('connector')
        self._http = HTTPClient(connector, loop=self._loop)

        self._token = token
        self._closed = asyncio.Event(loop=self._loop)
        self._ready = asyncio.Event(loop=self._loop)

    async def get_online(self, adult=False, gaming=False, categories=None):
        """
        This will return a OnlineChannel

        :param adult:
        :param gaming:
        :param categories:
        :return:
        """

        all_online = await self._http.get_online(adult, gaming, categories)
        return list(OnlineChannel(data=online) for online in all_online)

    async def get_categories(self):
        """

        Returns
        -------
        Generator of the categories in Picarto.

        """

        categories = await self._http.get_categories()
        return list(Category(data=category) for category in categories)

    async def get_channel_by_id(self, channel_id):
        data = await self._http.get_channel_by_id(channel_id)
        return Channel(data=data)

    async def get_channel_by_name(self, channel_name):
        data = await self._http.get_channel_by_name(channel_name)
        return Channel(data=data)

    async def get_full_channel(self, channel: OnlineChannel):
        return await self.get_channel_by_id(channel.user_id)
