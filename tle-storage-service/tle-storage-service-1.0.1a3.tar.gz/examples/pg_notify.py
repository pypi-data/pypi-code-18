#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import os

from aiopg import create_pool

from tle_storage_service import load_cfg, listen_pg_notify, LOG_FORMAT

DIR = os.path.abspath(os.path.dirname(__file__))
CFG = load_cfg(path=os.path.join(DIR, 'config', 'tle-storage-service.yaml'))

logger = logging.getLogger(__name__)


async def notify_callback(msg):
    logger.info('[%s] Receive msg <- "%s"', msg.channel, msg.payload)


async def listen_notifies(db_params, loop):
    async with create_pool(loop=loop, **db_params) as pool:
        await asyncio.wait([
            listen_pg_notify(pool, 'tle:space-track:update', callback=notify_callback),
            listen_pg_notify(pool, 'tle:nasa:update', callback=notify_callback)
        ])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_notifies(CFG['db'], loop))
