# -*- coding: utf-8 -*-

class MonguaLocked(Exception):
    def __init__(self, obj):
        self.data = obj
        self.msg = '[MongoMixin]: locked instance is not savable.'


class MonguaNotFound(Exception):
    def __init__(self, collection):
        self.msg = '[MongoMixin]: not found collection({})'.format(collection)


class MonguaKeyFrozen(Exception):
    def __init__(self, collection, field_key):
        self.msg = '[MongoMixin]: {}._frozen_key({}) is immutable.'.format(collection, field_key)


class MonguaKeyUndefined(Exception):
    def __init__(self, collection, field_key):
        self.msg = "[MongoMixin]: The Key({}) is undefined in {}.__fields__".format(field_key, collection)


class MonguaFieldUnmovable(Exception):
    def __init__(self, collection, field_key):
        self.msg = '[MongoMixin]: The Field({}) is still in {}.__fields__ '.format(field_key, collection)
