import requests

from codestats.bases import User as _User


class User(_User):
    def __init__(self, name: str, auto_load: bool=True, sync: bool=True):
        """
        Loads the user data into the instance by calling the ``load`` method. If
         you really want to, this method can be run in an Asyncio executor by setting
         ``sync`` to ``False``.
        Note: This will still block the event loop till it's complete.

        :param name: Name of the user as it's known as at the Code::Stats API.
        :param sync: Set to ``False`` if the user data should be loaded in an
            executor.
        """
        super().__init__(name, auto_load)

        if auto_load:
            self.load()

    def load(self):
        """
        Load and parse the user data from the Code::Stats API
        :raise ValueError: If the username is invalid
        """
        if self.name is None or self.name == "":
            raise ValueError("Username cannot be '{}'".format(self.name))

        uri = self.URL + self.name
        response = requests.get(uri)
        self._parse(response.json())
