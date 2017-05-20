# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from aiohttp import ClientSession
from nasa_tle_loader import NasaTLELoader, tle_list

from .log import logger as module_logger


class AsyncNasaTLELoader(NasaTLELoader):
    __slots__ = (
        'session',
    )

    def __init__(self, session=None, loop=None, **kwargs):
        kwargs.setdefault('logger', logging.getLogger('{}.{}'.format(module_logger.name, self.__class__.__name__)))
        super().__init__(**kwargs)

        self.session = session if isinstance(session, ClientSession) else ClientSession(loop=loop)

    async def load(self):
        async with self.session.get(self.url) as resp:
            return await resp.text()

    async def get(self, text=None):
        if not isinstance(text, str):
            text = await self.load()
        return tle_list(text)

    def close(self):
        self.session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        self.close()

    async def __call__(self, **kwargs):
        return await self.get(**kwargs)
