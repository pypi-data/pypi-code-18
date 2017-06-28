import copy
from threading import RLock

import scopeton.DiTools as DiTools
from scopeton.ContextBean import ContextBean

lock = RLock()


def _StaticSync(fn):
    def wrapped(*args, **kwargs):
        lock.acquire()
        try:
            return fn(*args, **kwargs)
        finally:
            lock.release()

    return wrapped


class StaticContext(object):
    _beans = {}  # type: dict[str, object]

    @classmethod
    @_StaticSync
    def getBeansCopy(cls):
        return copy.copy(cls._beans)

    @classmethod
    @_StaticSync
    def registerBean(cls, clazz, lazy=True, name=None):
        bean = DiTools.createBean(clazz, lazy=lazy)
        cls._beans[name or bean.name] = bean

def Service(lazy=True, name=None):
    def decorator(cls):
        StaticContext.registerBean(cls, lazy=lazy, name=name)
        return cls

    return decorator
