# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

try:
    import threading
except ImportError as e:
    import dummy_threading as threading


class RequestSessionFactory(object):
    def __init__(self, init=None):

        if init is None:
            init = {}

        self.storage = threading.local()
        self.storage.lazies = {}
        self.storage.concrete = {}
        self.lazies.update(init)

    @property
    def lazies(self):
        return self.storage.lazies

    @property
    def concrete(self):
        return self.storage.concrete

    def set_lazy(self, key, val):
        self.lazies[key] = val

    def guess(self, hint=None):
        return None

    def close(self):
        for key in self.lazies.keys():
            if self.concrete.has_key(key):
                session = self.concrete.get(key)
                close_key = "close"
                if hasattr(session, close_key):
                    close_callable = getattr(session, close_key)
                    if callable(close_callable):
                        close_callable()

    def __getattr__(self, attr):

        if attr not in self.lazies.keys():
            raise AttributeError("Invalid attribute: '%s'" % attr)

        if attr in self.concrete.keys():
            return self.concrete[attr]

        try:
            val = self.lazies[attr]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % attr)

        if callable(val):
            val = val()

        self.concrete[attr] = val
        return val