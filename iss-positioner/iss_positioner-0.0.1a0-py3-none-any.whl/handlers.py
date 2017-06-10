# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime, timedelta
from functools import partial
from json import JSONDecodeError

from aiohttp import web
from dateutil import parser as dt_parser

from .log import logger
from .redis import geo_radius, get_coords
from .util import datetime_range


async def get_json(request):
    try:
        data = await request.json()
    except JSONDecodeError:
        raise web.HTTPBadRequest(reason='Wrong JSON format')
    else:
        return data


def _validate_requires(required, iterable, *, is_body=True, msg=None):
    if not required.issubset(iterable):
        raise web.HTTPBadRequest(reason=msg or ('{} parameters must contains required keys `{}`'
                                                .format('Body' if is_body else 'Query', required)))


async def get(request):
    _validate_requires({'dt'}, request.query, is_body=False)
    data = request.query.copy()
    start_dt = end_dt = dt_parser.parse(data.pop('dt'))
    if start_dt < datetime(*datetime.today().timetuple()[:3]):
        raise web.HTTPNotFound
    coords = await get_coords(request.app['redis'], start_dt=start_dt, end_dt=end_dt, step=1, loop=request.app.loop)
    return coords


async def get_many(request):
    _validate_requires({'start_dt', 'end_dt'}, request.query, is_body=False)
    data = request.query.copy()
    dts = dt_parser.parse(data.pop('start_dt')), dt_parser.parse(data.pop('end_dt'))
    start_dt, end_dt = min(dts), max(dts)
    if start_dt < datetime(*datetime.today().timetuple()[:3]):
        raise web.HTTPNotFound
    step = int(data.get('step', '5'))
    coords = await get_coords(request.app['redis'], start_dt=start_dt, end_dt=end_dt, step=step, loop=request.app.loop)
    return coords


async def post(request):
    data = await get_json(request)
    _validate_requires({'start_dt', 'end_dt', 'lat', 'lon'}, data)
    dts = dt_parser.parse(data.pop('start_dt')), dt_parser.parse(data.pop('end_dt'))
    start_dt, end_dt = min(dts), max(dts)
    if start_dt < datetime(*datetime.today().timetuple()[:3]):
        raise web.HTTPNotFound
    return await compute_intersect(request.app['redis'], start_dt=start_dt, end_dt=end_dt, loop=request.app.loop,
                                   **data)


async def post_many(request):
    data = await get_json(request)
    _validate_requires({'objects', 'start_dt', 'end_dt'}, data)

    objects = data['objects']
    if not isinstance(objects, list):
        raise web.HTTPBadRequest(reason='Body parameter `objects` must be `array`')
    object_keys = {'lat', 'lon'}
    if not all(object_keys.issubset(obj) for obj in objects):
        raise web.HTTPBadRequest(reason='Object inside array `objects` '
                                        'must contains required keys `{}`'.format(object_keys))

    dts = dt_parser.parse(data.pop('start_dt')), dt_parser.parse(data.pop('end_dt'))
    start_dt, end_dt = min(dts), max(dts)
    if start_dt < datetime(*datetime.today().timetuple()[:3]):
        raise web.HTTPNotFound

    func = partial(compute_intersect,
                   redis=request.app['redis'],
                   start_dt=start_dt,
                   end_dt=end_dt,
                   loop=request.app.loop)
    return {obj.get('title', (obj['lon'], obj['lat'])): await func(**obj) for obj in objects}


async def index(request):
    html = '''
    <html>
        <head>
            <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
            <script>
                var channelName = 'coords';
                var source = new WebSocket('ws://' + window.location.host + '/subscribe/' + channelName);
                function eventListener(event) {
                    // var message = JSON.parse(event.data);
                    $('.messages').append([
                      $('<dt>').text(channelName),
                      $('<dd>').append($('<pre>').html(event.data)),
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
    channel_name = request.match_info['channel']
    channel = request.app['channels'][channel_name]
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    channel.add(ws)
    logger.debug('Someone joined to channel "{}".'.format(channel_name))

    try:
        while True:
            msg = await ws.receive_json()
            if msg.get('command') == 'close':
                await ws.close()
    except Exception as exc:
        logger.exception(exc)
    finally:
        channel.remove(ws)

    if ws.closed:
        channel.remove(ws)

    logger.debug('Websocket connection closed in channel "{}"'.format(channel_name))
    return ws


async def compute_intersect(redis, *, start_dt=None, end_dt=None, loop=None, **params):
    min_duration = params.pop('min_duration', None)
    rng = datetime_range(datetime(*start_dt.timetuple()[:4]), datetime(*end_dt.timetuple()[:4]), timedelta(hours=1))
    func = partial(geo_radius, redis=redis, **params)
    result = await asyncio.gather(*(func(dt=dt) for dt in rng), loop=loop)
    return filter(lambda val: len(val) > min_duration if min_duration else val, result)
