#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import partial

import ujson
from aiohttp import web, WSCloseCode
from aiopg.sa import create_engine

from .db import run_migrations
from .handlers import index, query, subscribe
from .log import logger
from .middlewares import json_response_middleware
from .utils import listen_pg_notify

__all__ = (
    'TleStorageService',
)


async def notify_callback(msg, app=None):
    if not app:
        return

    logger.debug('[%s] Receive msg <- "%s"', msg.channel, msg.payload)
    for ws in app['channels']:
        payload = ujson.loads(msg.payload)
        payload['channel'] = msg.channel
        ws.send_json(payload)


async def start_background_tasks(app):
    app['pg'] = await create_engine(**app['config']['db'], loop=app.loop)
    app['space_track_listener'] = app.loop.create_task(
        listen_pg_notify(app['pg'], 'tle:space-track:update', callback=partial(notify_callback, app=app))
    )

    app['nasa_listener'] = app.loop.create_task(
        listen_pg_notify(app['pg'], 'tle:nasa:update', callback=partial(notify_callback, app=app))
    )


async def cleanup_background_tasks(app):
    app['space_track_listener'].cancel()
    app['nasa_listener'].cancel()
    app['pg'].close()

    await app['space_track_listener']
    await app['nasa_listener']
    await app['pg'].wait_closed()


async def on_shutdown(app):
    for ws in app['channels']:
        await ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')


async def do_migrate(app):
    run_migrations(app['config']['db'])


class TleStorageService(web.Application):
    def __init__(self, *, config=None, **kwargs):
        if not isinstance(config, dict):
            raise ValueError('Argument `config` must be dict()')

        super().__init__(**kwargs)

        self.middlewares.append(json_response_middleware)
        self['config'] = config
        self['channels'] = set()
        self.on_startup.append(do_migrate)
        self.on_startup.append(start_background_tasks)
        self.on_cleanup.append(cleanup_background_tasks)
        self.on_shutdown.append(on_shutdown)
        self.router.add_get('/', index)
        self.router.add_get('/query', query)
        self.router.add_get('/subscribe', subscribe)
