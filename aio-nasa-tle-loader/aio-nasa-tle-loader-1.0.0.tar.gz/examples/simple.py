# -*- coding: utf-8 -*-

import asyncio
import json

from aio_nasa_tle_loader import AsyncNasaTLELoader


async def main(loop):
    async with AsyncNasaTLELoader(loop=loop) as loader:
        # Getting list `nasa_tle_loader.TLE`(namedtuple like) objects
        tle_list = await loader()

        # Print result as JSON
        print(json.dumps([tle.as_dict() for tle in tle_list[:3]], indent=2))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
