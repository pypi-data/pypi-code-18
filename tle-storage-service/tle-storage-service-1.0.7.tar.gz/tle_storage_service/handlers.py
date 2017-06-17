# -*- coding: utf-8 -*-

import sqlalchemy as sa
import ujson
from aiohttp import web, WSMsgType

from .db import TLE
from .log import logger
from .utils import parse_sa_filter, parse_sa_order, check_sa_column, get_sa_column


async def query(request):
    filters = []
    if 'filters' not in request.query:
        raise web.HTTPBadRequest(reason='Query parameter `filters` is required')

    try:
        _filters = ujson.loads(request.query.get('filters', '{}'))
        for k, v in _filters.items():
            filters.extend(parse_sa_filter(TLE, k, v))
    except ValueError:
        raise web.HTTPBadRequest(reason='Query parameter `filters` must contains valid JSON')

    _order = request.query.get('order', '{}')
    if _order.startswith('{'):
        try:
            order = ujson.loads(_order)
        except ValueError:
            raise web.HTTPBadRequest(reason='Query parameter `order` must contains valid JSON')
    else:
        order = _order

    order = parse_sa_order(TLE, order)
    only = [get_sa_column(TLE, key) for key in request.query.get('only', '').split(',') if check_sa_column(TLE, key)]

    async with request.app['pg'].acquire() as conn:
        rp = await conn.execute(sa.select(only or [TLE]).where(sa.and_(*filters)).order_by(*order))
    return [dict(r) async for r in rp]


async def index(request):
    html = '''
    <html>
        <head>
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <script>
                var source = new WebSocket('ws://' + window.location.host + '/subscribe');
                function eventListener(event) {
                    var message = JSON.parse(event.data);
                    $('.messages').append([
                      $('<dt>').text(message.channel),
                      $('<dd>').text(event.data),
                    ]);
                }
                source.onmessage = eventListener;
            </script>
        </head>
        <body>
            <dl class="messages"></dl>
        </body>
    </html>
    '''
    return web.Response(text=html, content_type='text/html')


async def subscribe(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['channels'].add(ws)
    logger.debug('Someone joined.')
    try:
        while True:
            msg = await ws.receive_json()
            if msg.get('command') == 'close':
                await ws.close()
    except Exception as exc:
        logger.exception(exc)
    finally:
        request.app['channels'].remove(ws)

    if ws.closed:
        request.app['channels'].remove(ws)

    logger.debug('websocket connection closed')
    return ws
