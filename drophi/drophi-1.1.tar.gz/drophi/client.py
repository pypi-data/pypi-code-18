import json
import logging
import time
import urllib.parse

import aiohttp
import arrow

LOGGER = logging.getLogger(__name__)

class CommunicationError(Exception):
    "Parent class for any communications errors with Docker"

class Client():
    def __init__(self):
        self.connector = aiohttp.UnixConnector(path='/var/run/docker.sock')
        self.session = aiohttp.ClientSession(connector=self.connector)

    def _url(self, path, **kwargs):
        if kwargs:
            return 'http://docker{}?{}'.format(path, '&'.join(["{}={}".format(k, v) for k, v in kwargs.items()]))
        else:
            return 'http://docker{}'.format(path)

    async def _get(self, path):
        url = self._url(path)
        async with self.session.get(url) as response:
            if not (response.status >= 200 and response.status < 300):
                raise CommunicationError("Failed to communicate with docker: status {} content {}".format(
                    response.status_code,
                    response.text,
                ))
            data = await response.json()
            return data

    async def close(self):
        LOGGER.debug("Closing aiohttp session")
        await self.session.close()

    async def ps(self):
        return await self._get('/containers/json')

    async def streamevents(self):
        LOGGER.debug("Subscribing to docker events")
        url = self._url('/events', since=time.time())
        data_buffer = b''
        text_buffer = ''
        async with self.session.get(url, timeout=0) as response:
            while True:
                data_buffer += await response.content.read(4096)
                try:
                    text_buffer += data_buffer.decode('utf-8')
                    data_buffer = b''
                except ValueError:
                    LOGGER.debug("Failed to decode data as UTF-8, waiting for more")
                    continue
                newline = text_buffer.find('\n')
                if newline:
                    message = text_buffer[:newline]
                    text_buffer = text_buffer[newline+1:]
                else:
                    LOGGER.debug("Waiting for more data to fine a newline and break off a message")
                    continue
                try:
                    data = json.loads(message)
                    yield Event(data)
                except ValueError:
                    LOGGER.error("Failed to parse JSON from '%s'", message)

class Event():
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return "Docker Event {} {} {} at {}".format(
            self.type,
            self.action,
            self.id,
            self.time,
        )

    @property
    def type(self):
        return self.data['Type']

    @property
    def action(self):
        return self.data['Action']

    @property
    def id(self):
        return self.data['id']

    @property
    def time(self):
        return arrow.get(self.data['time'])
