#!/usr/bin/env python3

from .log import system_log as _log

from typing import Iterable
from types import coroutine

import logging
import hmac

log = _log.getChild('objects')

DEFAULT_HMAC='sha256'
HMAC_KEY=b'epicman-server'
        
class ID(int):
    def __repr__(self):
        return f'ID({self})'

class Entity():
    def __new__(cls, id: ID, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj._epic_id = id
        
        log.debug("Creating object: %s[%r]", cls.__name__, id) 
        
        return obj
                
    @classmethod
    def _child_classes(cls):
        for child in cls.__subclasses__():
            yield from child._child_classes()
            yield child

    def load(self, data):
        self.__dict__ = data
        
        return self

    @coroutine
    def save(self) -> Iterable[dict]:
        return (yield CmdPersist(self.__dict__))

class Pool():
    def __init__(self, db):
        self.entites = {}
        self.live = {}
        self.db = db
        
    def bind(self, entities: Entity):
        self.entites.update({x.__name__: x for x in entities._child_classes()})

    def __getattr__(self, key):
        typ = self.entites[key]
        return TypeProxy(typ)

    def __getitem__(self, key):
        obj = self.live.get(key)
        if obj is None:
            typ, id = key
            obj = typ(id)
                        
            try:
                state = self.db[key]
                obj.load(state)
            except KeyError:
                pass

            self.live[key] = obj

        return obj


    async def call_object(self, typ: type, id: ID, method_name: str, args, kwargs):
        obj = self[(typ, id)]
        method = getattr(obj, method_name)
        if method is None:
            raise AttributeError(f"{typ.__name__} object has no attribute {method}")
        r = await method(*args, **kwargs)
        
        return r


class TypeProxy():
    _id: ID
    _method: str
    def __init__(self, typ):
        self._type = typ

    def __getitem__(self, id):
        self._id = id
        return self
    
    def __getattr__(self, name):
        self._method = name
        return self

    @coroutine    
    def __call__(self, *args, **kwargs):
        return (yield CmdRPC(self._type, self._id, self._method, args, kwargs))

    def __repr__(self):
        method = self._method if self._method != '_method' else ''
        return f'{self._type.__name__}[{self._id}]' + method

    def __getstate__(self):
        return (self._type, self._id, self._method)

    def __setstate__(self, args):
        self._type, self._id, self._method = args

# there is an import loop with 'cmds' module (requires Entity)
# so we ensure that we dont do the import until Entity is set
# up in this namesapce
from .cmds import CmdRPC, CmdPersist
