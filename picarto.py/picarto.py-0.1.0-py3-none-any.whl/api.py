import asyncio
import enum
import json
import logging
import sys

import aiohttp

from . import errors

log = logging.getLogger(__name__)
log.debug("TEST")


async def json_or_text(response):
    text = await response.text(encoding='utf-8')
    logging.info(response.headers['Content-Type'])
    if 'application/json' in response.headers['Content-Type']:
        return json.loads(text)
    return text


class Methods(enum.Enum):
    GET = 'GET'
    POST = 'POST'


class Route:
    BASE = 'https://api.picarto.tv/v1'

    def __init__(self, method, path, **parameters):
        self.path = path
        self.method = method
        self.url = self.BASE + self.path
        if parameters:
            self.url = self.url.format(**parameters)


class HTTPClient:
    """Represents an HTTP client sending HTTP requests to the Picarto API."""

    SUCCESS_logging = '{method} {url} has received {text}'
    REQUEST_logging = '{method} {url} with {json} has returned {status}'

    def __init__(self, connector=None, *, loop=None):
        self.loop = loop if loop else asyncio.get_event_loop()
        self.connector = connector
        self._session = aiohttp.ClientSession(connector=connector, loop=self.loop)
        self.token = None

        user_agent = 'PicartoBot (https://github.com/ivandardi/picarto.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format('0.1.0', sys.version_info, aiohttp.__version__)

    async def request(self, route, **kwargs):
        headers = {
            'Accept'      : 'application/json',
            'Content-Type': 'application/json',
            'User-Agent'  : self.user_agent,
        }
        kwargs['headers'] = headers

        method = route.method.value
        async with self._session.request(method, route.url, **kwargs) as r:
            log.debug(
                self.REQUEST_logging.format(method=method, url=route.url, status=r.status, json=kwargs.get('data')))

            data = await json_or_text(r)

            if 200 <= r.status < 300:
                log.debug(self.SUCCESS_logging.format(method=method, url=route.url, text=data))
                return data

            if r.status == 403:
                raise errors.Forbidden(r, data)
            elif r.status == 404:
                raise errors.NotFound(r, data)
            else:
                raise errors.HTTPException(r, data)

    # Public functionality

    def get_online(self, adult=False, gaming=False, categories=None):
        route = Route(Methods.GET, '/online')

        params = json.dumps({
            'adult'     : adult,
            'gaming'    : gaming,
            'categories': ','.join(categories) if categories else ''
        })

        return self.request(route, params=params)

    def get_categories(self):
        route = Route(Methods.GET, '/categories')
        return self.request(route)

    # Channel functionality

    def get_channel_by_id(self, channel_id: int):
        route = Route(Methods.GET, '/channel/id/{channel_id}', channel_id=channel_id)
        return self.request(route)

    def get_channel_by_name(self, channel_name: int):
        route = Route(Methods.GET, '/channel/name/{channel_name}', channel_name=channel_name)
        return self.request(route)
