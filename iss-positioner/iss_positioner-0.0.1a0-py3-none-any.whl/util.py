# -*- coding: utf-8 -*-
import asyncio
import os
import ujson
from datetime import datetime, timedelta
from functools import wraps

import yaml
from aiohttp import ClientSession

from .log import logger

__all__ = (
    'PROJECT_DIR',
    'load_cfg',
    'periodic_task',
    'audit',
)

PROJECT_DIR = os.path.join(os.path.dirname(__file__))


def load_cfg(*, filename='dev', path=None):
    if not isinstance(path, str):
        path = os.path.join(PROJECT_DIR, 'config', '{}.{}'.format(filename, 'yaml'))

    if not os.path.exists(path):
        raise FileNotFoundError

    with open(path, 'r') as cfg:
        return yaml.safe_load(cfg)


def periodic_task(delay):
    def wrapper(coroutine):
        @wraps(coroutine)
        async def runner(*args, **kwargs):
            while True:
                await coroutine(*args, **kwargs)
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


def datetime_range(start, end, step=None):
    if not isinstance(start, datetime) or not isinstance(end, datetime):
        raise ValueError

    if not isinstance(step, timedelta):
        step = timedelta(seconds=step or 1)

    if start == end:
        yield start

    while start < end:
        yield start
        start += step


async def get_tle(*, url=None, loop=None):
    d = datetime.today().date() - timedelta(days=1)
    query = {
        "filters": ujson.dumps({"dt": {"$gte": d.isoformat()}, "norad_cat_id": 25544}),
        "order": "dt",
        "only": "id,source,extra_info"
    }
    async with ClientSession(loop=loop) as session:
        async with session.get(url, params=query) as resp:
            r = await resp.json(loads=ujson.loads)
    return r.get('data')
