# coding: utf8

# Copyright 2013-2015 Vincent Jacques <vincent@vincent-jacques.net>

import inspect

from . import MockException


class Replacer(object):
    def __init__(self):
        self.__replaced = []

    def replace(self, name, mock):
        container, attribute = self.__find(name)
        self.__replaced.append((container, attribute, getattr(container, attribute)))
        setattr(container, attribute, mock.object)

    @staticmethod
    def __find(name):
        names = name.split(".")
        attribute = names[-1]
        current = inspect.currentframe()
        try:
            frame = current.f_back.f_back.f_back
            symbols = dict(frame.f_globals)
            symbols.update(frame.f_locals)
            container = symbols.get(names[0])
        finally:
            del current
        if container is None:
            raise MockException("Unable to replace {}".format(name))
        for part in names[1:-1]:
            if not hasattr(container, part):
                raise MockException("Unable to replace {}".format(name))
            container = getattr(container, part)
        if not hasattr(container, attribute):
            raise MockException("Unable to replace {}".format(name))
        return container, attribute

    def tear_down(self):
        for container, attribute, value in self.__replaced:
            setattr(container, attribute, value)
