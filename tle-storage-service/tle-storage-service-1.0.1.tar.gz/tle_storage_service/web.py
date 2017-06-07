# -*- coding: utf-8 -*-
from functools import partial

import ujson
from aiohttp import web

__all__ = (
    'json_response',
)

json_response = partial(web.json_response, dumps=ujson.dumps)
