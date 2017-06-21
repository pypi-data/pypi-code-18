import asyncio
import asyncio.subprocess
import logging

import aiohttp
import maxillo.deployments
import maxillo.networking

LOGGER = logging.getLogger(__name__)

async def handle_message(app, session, host, message):
    type_ = message.get('type', None)
    host = host or maxillo.deployments.load_license().master
    try:
        LOGGER.info("Handling %s message", type_)
        if type_ == 'command':
            await _handle_command(app, session, host, message)
        elif type_ == 'deployment':
            await _handle_deployment(app, session, host, message)
        else:
            LOGGER.warning("Ignoring unexpected message type '%s'", type_)
    except Exception as e:
        LOGGER.exception("Failed to properly handle message %s", message)

class CommandProtocol(asyncio.SubprocessProtocol):
    def __init__(self, session, host, message, exit_future):
        self.exit_future    = exit_future
        self.host           = host
        self.message        = message
        self.session        = session
        self.stderr         = bytearray()
        self.stderr_stream  = asyncio.StreamReader()
        self.stderr_request = None
        self.stdout         = bytearray()
        self.stdout_stream  = asyncio.StreamReader()
        self.stdout_request = None
        self.transport      = None

    async def feed_stream(writer):
        while True:
            chunk = await self.stdout_queue.get()

    async def _begin_request(self):
        headers = maxillo.deployments.generate_auth_headers('chunked')
        url = '{}/deployment/{}/command/{}'.format(self.host, self.message['deployment'], self.message['uuid'])
        proxy = maxillo.networking.get_proxy()

        self.stdout_request = await self.session.post(
            url + '/stdout/',
            headers = headers,
            timeout = 0,
            data = self.stdout_stream,
            proxy = proxy
        )

        self.stderr_request = await self.session.post(
            url + '/stderr/',
            headers = headers,
            timeout = 0,
            data = self.stderr_stream,
            proxy = proxy
        )

    def connection_made(self, transport):
        LOGGER.debug("Connection made to %s", self.message)
        self.transport = transport
        asyncio.ensure_future(self._begin_request())

    def pipe_data_received(self, fd, data):
        LOGGER.debug("Got data %s on %s", data, fd)
        if fd == 1:
            self.stdout_stream.feed_data(data)
        elif fd == 2:
            self.stderr_stream.feed_data(data)
        else:
            LOGGER.error("Unexpected fd %s", fd)

    def connection_lost(self, exc):
        LOGGER.debug("Connection lost to subprocess for %s. exc: %s", self.message, exc)

    def process_exited(self):
        return_code = self.transport.get_returncode()
        LOGGER.debug("Process exited for %s with status %s", self.message, return_code)
        self.exit_future.set_result(return_code)
        self.stdout_stream.feed_eof()
        self.stderr_stream.feed_eof()
        asyncio.ensure_future(self._send_result())

    async def _send_result(self):
        return_code = self.transport.get_returncode()
        url = '{}/deployment/{}/command/{}/'.format(self.host, self.message['deployment'], self.message['uuid'])
        headers = maxillo.deployments.generate_auth_headers('chunked')
        payload = {'result': return_code}
        proxy = maxillo.networking.get_proxy()
        async with self.session.put(url, data=payload, headers=headers, proxy=proxy) as response:
            LOGGER.debug("Status code %s sent to master at %s with response %s", return_code, url, response.status)

async def _handle_command(app, session, host, message):
    exit_future = asyncio.Future()
    loop = asyncio.get_event_loop()
    create = loop.subprocess_shell(
        lambda: CommandProtocol(session, host, message, exit_future),
        message['command'],
        stdout  = asyncio.subprocess.PIPE,
        stderr  = asyncio.subprocess.PIPE,
    )
    transport, protocol = (await create)
    await exit_future
    transport.close()
    LOGGER.info("Completed running command %s: %s", message['uuid'], message['command'])

async def _handle_deployment(app, session, host, message):
    app['deployment'] = message
