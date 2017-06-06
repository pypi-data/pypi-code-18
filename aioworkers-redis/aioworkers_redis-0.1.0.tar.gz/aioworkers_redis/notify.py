import asyncio
import time

import aioredis
from aioworkers.queue.base import AbstractQueue
from aioworkers.storage.base import AbstractStorage

from aioworkers_redis.base import Connector


class Notifier(Connector, AbstractStorage, AbstractQueue):
    async def init(self):
        await super().init()
        self._lock = asyncio.Lock(loop=self.loop)
        self._key = self.config.get('key')
        if self._key is not None:
            self._key = self.raw_key(self._key)

    async def put(self, value):
        value = self.encode(value)
        async with self.pool as conn:
            return await conn.publish(self._key, value)

    async def get(self, key=None):
        await self._lock.acquire()
        try:
            async with self.pool as conn:
                result = await conn.blpop(self._key)
            self._lock.release()
        except aioredis.errors.PoolClosedError:
            await self._lock.acquire()
        value = self.decode(result[-1])
        return value
