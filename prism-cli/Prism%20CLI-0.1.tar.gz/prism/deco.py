#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

from functools import wraps

from . import log


def save_app(func):
    def wrapper(app, *args, **kwargs):
        ret = func(app, *args, **kwargs)
        app.save_config()
        return ret
    return wrapper

def header(text):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.header(text)
            return func(*args, **kwargs)
        return wrapper
    return decorator

def require_app(inverse=False):
    def decorator(func):
        @wraps(func)
        def wrapper(app, *args, **kwargs):
            if inverse:
                if app.is_created:
                    log.fail('Application already exists!')
                    return
            else:
                if not app.is_created:
                    log.fail('No application with that name!')
                    return
            return func(app, *args, **kwargs)
        return wrapper
    if callable(inverse):
        func = inverse
        inverse = False
        return decorator(func)
    return decorator

def log_group(start, end):
    def decorator(func):
        @wraps(func)
        def wrapper(app, *args, **kwargs):
            log.doing(start)
            log.level += 1
            ret = func(app, *args, **kwargs)
            log.level -= 1
            log.doing(end)
            return ret
        return wrapper
    return decorator
