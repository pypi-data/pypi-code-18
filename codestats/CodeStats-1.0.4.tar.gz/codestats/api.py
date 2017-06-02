try:
    import asyncio

    async_enabled = True
except ImportError:
    async_enabled = False

import datetime
import math
from typing import List

import requests


LEVEL_FACTOR = 0.025


def calculate_level(experience: int, level_factor: float=LEVEL_FACTOR) -> int:
    """
    Calculate the current level based on the provided experience and level factor. The
     same formula is used as the official API / website.

    :param experience: The experience to calculate the level of
    :param level_factor: The level factor to use, defaults to ``LEVEL_FACTOR`` (0.025)
    :return:The level as an integer
    """
    return int(math.floor(level_factor * math.sqrt(experience)))


def calculate_next_level_xp(experience: int=None, level: int=None, level_factor: float=LEVEL_FACTOR) -> int:
    """
    Calculate how much experience is needed to reach the next level. If a level if provided
     this used, otherwise the provided experience is used to first calculate the level.
    :param experience: The experience to calculate the level if no level was provided
    :param level: The current level
    :param level_factor: The level factor to use, defaults to ``LEVEL_FACTOR`` (0.025)
    :return: The experience needed as an integer
    :raise ValueError: If ``experience`` and ``level`` are both ``None``.
    """
    if level is None and experience is not None:
        level = calculate_level(experience)
    elif level is None and experience is None:
        raise ValueError("'Experience' and 'level' cannot both be None")

    return int(math.pow(math.ceil((level + 1) / level_factor), 2))


def calculate_progress(experience: int) -> float:
    """
    Calculate the progress to the next level as a percentage.
    :param experience: The current experience
    :return: The percentage as a float
    """
    level = calculate_level(experience)
    current_level_xp = calculate_next_level_xp(level=level - 1)
    next_level_xp = calculate_next_level_xp(level=level)

    have_xp = experience - current_level_xp
    needed_xp = next_level_xp - current_level_xp

    return (have_xp / needed_xp) * 100


class BaseObject(object):
    def __init__(self, name, xps: int, new_xps: int=None):
        self.name = name
        self.experience = xps
        self.new_experience = new_xps

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)

    @property
    def level(self) -> int:
        return calculate_level(self.experience)

    @property
    def next_level(self) -> int:
        return calculate_next_level_xp(self.experience)

    @property
    def progress(self) -> float:
        return calculate_progress(self.experience)


class Machine(BaseObject):
    pass


class Language(BaseObject):
    pass


class Date(object):
    """ Does not inherit from ``BaseObject`` as the experience structure is  """
    def __init__(self, date, experience):
        self.date = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.experience = experience


class LocalPulse(object):
    def __init__(self, language: Language, xp: int):
        self.language = language
        self.xp = xp


class Pulse(object):
    def __init__(self, xps: List[Language]):
        self.coded_at = datetime.datetime.now().isoformat()
        self.xps = xps

    def serialize(self) -> dict:
        return {
            'coded_at': self.coded_at,
            'xps': self.xps
        }


class User(object):
    __slots__ = ("name", "total_xp", "new_xp", "user", "machines", "languages", "dates", "last_pulse", "token")

    URL = "https://codestats.net/api/users/"
    TYPES = {
        'machines': Machine,
        'languages': Language,
    }

    def __init__(self, name: str, auto_load: bool=True, sync: bool=True, token: str=None):
        """
        Loads the user data into the instance by calling the ``load`` method. If
         you really want to, this method can be run in an Asyncio executor by setting
         ``sync`` to ``False``.
        Note: This will still block the event loop till it's complete.

        :param name: Name of the user as it's known as at the Code::Stats API.
        :param sync: Set to ``False`` if the user data should be loaded in an
            executor.
        """
        self.name = name
        self.token = token

        if auto_load:
            if sync:
                self.load()
            elif async_enabled:
                coro = asyncio.coroutine(self.load)
                loop = asyncio.get_event_loop()
                loop.run_until_complete(coro())
            else:
                raise ValueError("AsyncIO is not installed")

    def load(self):
        """
        Load and parse the user data from the Code::Stats API
        :raise ValueError: If the username is invalid
        """
        if self.name is None or self.name == "":
            raise ValueError("Username cannot be '{}'".format(self.name))

        uri = self.URL + self.name
        response = requests.get(uri)
        self._parse(response)

    def add(self, language: Language, xp: int):
        lp = LocalPulse(language, xp)
        self.add_pulse(lp)

    def add_pulse(self, pulse: LocalPulse, auto_pulse: bool=False):
        pass

    def pulse(self):
        """
        Send the local pulses to the API
        :return:
        """
        if self.token is None:
            raise ValueError("A token is required but is 'None'")
        pass

    def _parse(self, response: requests.Response):
        """
        Parses the response we got from the API
        :param response: Response body to parse
        :raise ValueError: If we receive an error from the API
        """
        data = response.json()
        error = data.get("error")

        if error is not None:
            raise ValueError(error)

        for key, value in data.items():
            if key in self.TYPES.keys():
                cls = self.TYPES[key]
                value = [cls(name, **xp) for name, xp in value.items()]
            elif key == "dates":
                value = [Date(date, xp) for date, xp in value.items()]

            setattr(self, key, value)

    def get(self, name: str, cls, ignore_case: bool=True):
        """
        Attempt to find an object related to the user based on the class and the name.

        :param name: Name of the object to find
        :param cls: Class to find. Eg: Machine or Language
        :param ignore_case: Convert the object's name as well as the provided name to
            lower case to make the search case insensitive.
        :return: The found instance
        :raise ValueError: If the value wasn't found
        """
        attr = self._get_attribute(cls)
        items = getattr(self, attr)
        for item in items:
            if (ignore_case and item.name.lower() == name.lower()) or \
                    item.name == name:
                return item

        raise ValueError("'{}' not found in {}".format(name, items))

    def _get_attribute(self, cls):
        """
        Find the attribute name using reverse lookup in the ``TYPES`` class
         constant.

        :param cls: Class to find
        :return:  The name of the attribute matching the class
        :raise AttributeError: If the class is not found and the attribute
            therefore shouldn't exist.
        """
        for key, value in self.TYPES.items():
            if value == cls:
                return key

        raise AttributeError

    def get_machine(self, name: str, ignore_case: bool=True):
        """
        Shorthand around the ``get`` method. Pre populate the class variable

        :param name: Name of the machine to find
        :param ignore_case: Make the search case sensitive
        :return:
        """
        return self.get(name, Machine, ignore_case)

    def get_language(self, name: str, ignore_case: bool=True):
        """
        Shorthand around the ``get`` method. Pre populate the class variable

        :param name: Name of the language to find
        :param ignore_case: Make the search case sensitive
        :return:
        """
        return self.get(name, Language, ignore_case)

    @property
    def level(self) -> int:
        return calculate_level(self.total_xp)

    @property
    def next_level(self) -> int:
        return calculate_next_level_xp(self.total_xp)

    @property
    def progress(self) -> float:
        return calculate_progress(self.total_xp)

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.name)
