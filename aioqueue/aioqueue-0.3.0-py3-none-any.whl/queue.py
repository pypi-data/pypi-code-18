import aioamqp
import asyncio
import umsgpack as msgpack
import signal
from .task import Task
from .response import Response
from .logger import logger

class Queue(object):
    def __init__(self, name, host='localhost', port=None, ssl=False, log_level=None, retry=5,
                 raw=False, durable=True, prefetch_count=1, prefetch_size=0, connection_global=False,
                 **connect_kwargs):
        self.name = name
        self.host = host
        self.port = port if port is not None else 5671 if ssl else 5672
        self.ssl = ssl
        self.retry = retry
        self._transport = None
        self._protocol = None
        self._channel = None
        self._connect_kwargs = connect_kwargs
        self._handler = None
        self._options = {
            'queue': {
                'durable': durable
            },
            'qos': {
                'prefetch_count': prefetch_count,
                'prefetch_size': prefetch_size,
                'connection_global': connection_global
            },
            'handler': {
                'raw': raw
            }
        }

        if log_level is not None:
            logger.setLevel(log_level)

    async def connect(self):
        if self.retry is not False:
            while self._protocol is None:
                try:
                    self._transport, self._protocol = await aioamqp.connect(host=self.host, port=self.port, ssl=self.ssl, **self._connect_kwargs)
                except:
                    logger.warn(f'Could not connect to amqp://{self.host}:{self.port}/. Trying again in {self.retry} second(s).')
                    await asyncio.sleep(self.retry)
        else:
            self._transport, self._protocol = await aioamqp.connect(host=self.host, port=self.port, ssl=self.ssl, **self._connect_kwargs)

        logger.info(f'Connected to amqp://{self.host}:{self.port}/.')
        self._channel = await self._protocol.channel()

    @staticmethod
    def _make_consumer(task_name, handler, raw=False):
        async def consumer(channel, body, envelope, properties):
            corr_id = properties.correlation_id
            response = Response(channel, envelope, properties)

            try:
                data = msgpack.unpackb(body) if not raw else body
                logger.info(f'Received request for {task_name} ({corr_id})')
                logger.debug(f'[{corr_id}][\'data\'] = {data}')
            except Exception as err:
                logger.error(f'Could not unpack message: {err} ({corr_id})')
                await response.send(err, None)
                return

            try:
                if asyncio.iscoroutinefunction(handler):
                    logger.debug(f'Calling coroutine {handler} ({corr_id})')
                    result = await handler(data)
                    logger.debug(f'Coroutine {handler} returned with {result} ({corr_id})')
                else:
                    logger.debug(f'Calling function {handler} ({corr_id})')
                    result = handler(data)
                    logger.debug(f'Function {handler} returned with {result} ({corr_id})')
            except Exception as err:
                logger.error(f'Exception while executing {task_name}: {err} ({corr_id})')
                await response.send(err, None)
                return

            await response.send(None, result)
        return consumer

    async def task(self, data, no_response=False, raw=False):
        logger.debug(f'Creating a new channel for task on queue `{self.name}`')

        logger.debug(f'Channel created. Creating task on queue `{self.name}` with data: {data}')
        task = Task(self.name, data, self._channel, no_response=no_response, raw=raw)
        logger.debug(f'Task created: {task}')
        await task.send()
        return task

    async def start_async(self):
        await self.connect()
        await self._channel.queue_declare(queue_name=self.name, **self._options['queue'])
        await self._channel.basic_qos(**self._options['qos'])
        if self._handler is not None:
            await self._channel.basic_consume(self._make_consumer(self.name, self._handler, **self._options['handler']), queue_name=self.name)
            logger.info(f'Consuming on queue {self.name}.')

    def start(self):
        loop = asyncio.get_event_loop()

        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame), loop.stop)

        loop.run_until_complete(self.start_async())
        try:
            loop.run_forever()
        finally:
            loop.close()

    async def close(self):
        await self._protocol.close()
        self._transport.close()

    def __call__(self, func):
        self._handler = func
        return func

    async def __aenter__(self):
        await self.start_async()

    async def __aexit__(self):
        await self.close()