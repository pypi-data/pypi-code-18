# -*- coding: utf-8 -*-
import json
from datetime import datetime

import sqlalchemy as sa
from aiopg.sa.result import ResultProxy

from .db import TLE, insert_tle
from .log import logger
from .utils import audit, send_pg_notify

__all__ = (
    'get_tle_dt',
    'nasa',
    'space_track',
)


@audit(logger=logger)
async def space_track(engine, api, satellites):
    satellites = {norad_cat_id: None for norad_cat_id in satellites}

    async with engine.acquire() as conn:

        satellites.update({row.norad_cat_id: row.dt async for row in get_latest_dt(conn)})

        for norad_cat_id, dt in satellites.items():
            params = dict(NORAD_CAT_ID=norad_cat_id)
            if dt:
                params['EPOCH'] = '>{:%Y-%m-%d %H:%M:%S}'.format(dt)

            tles = await api.tle(**params)
            if isinstance(tles, str):
                raise KeyboardInterrupt(tles)

            got_count = len(tles)

            logger.debug('[%s] Got %d tle', space_track.__name__, got_count)

            result = await store_tles(conn, convert_tles(tles))
            store_count = result.rowcount if isinstance(result, ResultProxy) else 0

            logger.debug('[%s] Stored %d tle', space_track.__name__, store_count)

            await send_pg_notify(conn, 'tle:space-track:update', json.dumps(dict(got=got_count,
                                                                                 stored=store_count)))


@audit(logger=logger)
async def nasa(engine, api):
    async with engine.acquire() as conn:
        tles = (tle.as_dict() for tle in await api.get())
        values = [tle for tle in convert_tles(tles, 'nasa')]

        got_count = len(values)
        logger.debug('[%s] Got %d tle', nasa.__name__, got_count)
        if not got_count:
            return

        expires = await delete_expires_tle(conn)
        expires_count = expires.rowcount if expires else 0
        logger.debug('[%s] Expires %d tle', nasa.__name__, expires_count)

        dts = [row.dt async for row in get_latest_dt(conn, norad_cat_id=25544)]
        if dts:
            max_dt = max(dts)
            values = filter(lambda value: value['dt'] > max_dt, values)

        result = await store_tles(conn, values)
        store_count = result.rowcount if isinstance(result, ResultProxy) else 0
        logger.debug('[%s] Stored %d tle', nasa.__name__, store_count)

        await send_pg_notify(conn, 'tle:nasa:update', json.dumps(dict(got=got_count,
                                                                      stored=store_count,
                                                                      expires=expires_count)))


def get_tle_dt(tle):
    return datetime.strptime('{EPOCH}.{EPOCH_MICROSECONDS}'.format(**tle), '%Y-%m-%d %H:%M:%S.%f')


def get_latest_dt(conn, source=None, norad_cat_id=None):
    if source is None:
        source = 'space-track'

    stmt = sa.select([
        TLE.c.norad_cat_id, sa.func.max(TLE.c.dt).label('dt')
    ]).where(
        TLE.c.source == source
    ).group_by(
        TLE.c.norad_cat_id
    )

    if isinstance(norad_cat_id, int):
        stmt = stmt.where(TLE.c.norad_cat_id == norad_cat_id)
    elif isinstance(norad_cat_id, list):
        stmt = stmt.where(TLE.c.norad_cat_id.in_(norad_cat_id))

    return conn.execute(stmt)


def convert_tles(tles, source=None):
    if not isinstance(source, str):
        source = 'space-track'

    return [
        dict(norad_cat_id=tle['NORAD_CAT_ID'],
             dt=get_tle_dt(tle),
             tle_line1=tle['TLE_LINE1'],
             tle_line2=tle['TLE_LINE2'],
             extra_info={k.lower(): v for k, v in tle.items()},
             source=source)
        for tle in tles
    ]


async def store_tles(conn, tles):
    if not tles:
        return
    if not isinstance(tles, list):
        tles = list(tles)
    return await insert_tle(conn, tles)


async def delete_expires_tle(conn):
    return await conn.execute(TLE.delete().where(TLE.c.source == 'nasa').returning(TLE))
