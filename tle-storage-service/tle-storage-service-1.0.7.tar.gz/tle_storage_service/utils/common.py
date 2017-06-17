# -*- coding: utf-8 -*-
import asyncio
import os
from datetime import datetime
from functools import wraps

import yaml

from ..log import logger

__all__ = (
    'PROJECT_DIR',
    'load_cfg',
    'periodic_task',
    'audit',
)

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)


def load_cfg(*, filename='dev', path=None):
    if not isinstance(path, str):
        path = os.path.join(PROJECT_DIR, 'config', '{}.{}'.format(filename, 'yaml'))

    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path, 'r') as cfg:
        return yaml.safe_load(cfg)


def periodic_task(delay, retry=30):
    def wrapper(coroutine):
        @wraps(coroutine)
        async def runner(*args, **kwargs):
            while True:
                try:
                    await coroutine(*args, **kwargs)
                except RuntimeError:
                    raise KeyboardInterrupt
                except Exception:
                    logger.exception('Task %r raise exception', coroutine)
                    await asyncio.sleep(retry)
                else:
                    await asyncio.sleep(delay)

        return runner

    return wrapper


def audit(*args, **kwargs):
    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            dt = datetime.now()
            log.debug('Start execution `%s`', func.__name__)
            result = func(*args, **kwargs)
            log.debug('End execution `%s` (%s)', func.__name__, datetime.now() - dt)
            return result

        @wraps(func)
        async def async_inner_wrapper(*args, **kwargs):
            dt = datetime.now()
            log.debug('Start execution `%s`', func.__name__)
            result = await func(*args, **kwargs)
            log.debug('End execution `%s` (%s)', func.__name__, datetime.now() - dt)
            return result

        log = kwargs.pop('logger', logger)

        return async_inner_wrapper if asyncio.iscoroutinefunction(func) else inner_wrapper

    if args and kwargs:
        raise ValueError("cannot combine positional and keyword args")
    if len(args) == 1:
        return wrapper(args[0])
    elif len(args) != 0:
        raise ValueError("expected 1 argument, got %d", len(args))
    return wrapper
