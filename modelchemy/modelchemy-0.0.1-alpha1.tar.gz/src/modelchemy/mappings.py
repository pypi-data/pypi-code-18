# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

class SiteMaps(object):

    def __init__(self):
        self._registry = {}

    def __getattr__(self, key):
        return self.get(key)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    @property
    def registry(self):
        return self._registry

    def get(self, key):
        return self.storage_get(key)

    def set(self, key, value):
        self.__storage_set(key, value)

    def storage_get(self, key):
        if key not in self.registry.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        try:
            val = self.registry[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        return val

    def __storage_set(self, key, value):
        self.registry[key] = value


maps = SiteMaps()