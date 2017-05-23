# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class SiteDatabaseRecordFactory(object):

    @property
    def factories(self):
        return self._factories

    @property
    def memoized(self):
        return self._memoized

    def __getattr__(self, attr):
        return self.__storage_get(attr)

    def __getitem__(self, item):
        return self.__storage_get(item)

    def __storage_get(self, key):
        if key not in self.factories.keys():
            raise AttributeError("Invalid attribute: '%s'" % key)

        if key in self.memoized.keys():
            return self.memoized[key]

        try:
            val = self.factories[key]
        except KeyError:
            raise AttributeError("Invalid attribute: '%s'" % key)

        if callable(val):
            val = val()

        self.memoized[key] = val
        return val

    def generate_metadata(self):
        metadata = MetaData()
        metadata.bind = self.engine
        return metadata

    def generate_base(self):
        return declarative_base(metadata=self.metadata)

    def generate_session(self):
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        return Session

    def generate_engine(self, url):
        def factory():
            return create_engine(url)
        return factory

    def __init__(self, url):
        self._factories = {}
        self._memoized = {}

        self.factories.update({
            'engine': self.generate_engine(url),
            'metadata': self.generate_metadata,
            'base': self.generate_base,
            'Session' : self.generate_session,
        })


class SiteDatabasesRegistry(object):

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

    @property
    def keys(self):
        return self.registry.keys()

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

        if not isinstance(value, SiteDatabaseRecordFactory):
            raise AttributeError("Invalid value for key: '%s'" % key)

        self.registry[key] = value

dbs = SiteDatabasesRegistry()
