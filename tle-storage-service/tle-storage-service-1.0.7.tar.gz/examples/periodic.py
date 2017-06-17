#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import logging
import os

from aio_nasa_tle_loader import AsyncNasaTLELoader
from aio_space_track_api import AsyncSpaceTrackApi
from aiopg.sa import create_engine

from tle_storage_service import periodic_task, load_cfg, nasa, space_track, LOG_FORMAT, run_migrations

DIR = os.path.abspath(os.path.dirname(__file__))
CFG = load_cfg(path=os.path.join(DIR, 'config', 'tle-storage-service.yaml'))

logger = logging.getLogger(__name__)


@periodic_task(CFG['sync'].get('space-track', 4) * 3600)
async def call_space_track(engine, api_params, satellites, loop):
    async with AsyncSpaceTrackApi(loop=loop, **api_params) as api:
        await space_track(engine, api, satellites)


@periodic_task(CFG['sync'].get('nasa', 0.5) * 3600)
async def call_nasa(engine, loop):
    async with AsyncNasaTLELoader(loop=loop) as loader:
        await nasa(engine, loader)


async def run(db_params, api_params, satellites, loop):
    async with create_engine(loop=loop, **db_params) as engine:
        await asyncio.gather(
            call_nasa(engine, loop),
            call_space_track(engine, api_params, satellites, loop),
            loop=loop
        )


if __name__ == '__main__':
    logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)

    run_migrations(CFG['db'])

    loop = asyncio.get_event_loop()
    try:
        loop.create_task(run(CFG['db'],
                             CFG['space-track'],
                             CFG['sync']['satellites'],
                             loop))
        loop.run_forever()
    finally:
        loop.close()
