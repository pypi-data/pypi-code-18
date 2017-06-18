import sys
from inspect import isclass


def findclass(func):
    """
    https://github.com/python/cpython/blob/master/Lib/inspect.py
    """
    cls = sys.modules.get(func.__module__)
    if cls is None:
        return None
    for name in func.__qualname__.split('.')[:-1]:
        try:
            cls = getattr(cls, name)
        except Exception as e:
            return None
    if not isclass(cls):
        return None
    return cls


def before(middleware):
    def decorator(func):
        def wrapper(*arguments, **keywords):
            middleware(*arguments, **keywords)
            return func(*arguments, **keywords)
        return wrapper
    return decorator


def after(middleware):
    def decorator(func):
        def wrapper(*arguments, **keywords):
            result = func(*arguments, **keywords)
            return middleware(result)
        return wrapper
    return decorator
