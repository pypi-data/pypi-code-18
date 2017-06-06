import datetime
import json

from codestats.levels import calculate_level, calculate_next_level_xp, calculate_progress


class BaseObject(object):
    def __init__(self, name, xps: int, new_xps: int):
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


class User(object):
    __slots__ = ("name", "total_xp", "new_xp", "user", "machines", "languages", "dates", "auto_load")

    URL = "https://codestats.net/api/users/"
    TYPES = {
        'machines': Machine,
        'languages': Language,
    }

    def __init__(self, name: str, auto_load: bool=True):
        self.name = name
        self.auto_load = auto_load

    def _parse(self, data: dict):
        """
        Parses the response we got from the API
        :param data: Decoded JSON response
        :raise ValueError: If we receive an error from the API
        """
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
