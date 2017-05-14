import asyncio
import json
import logging
from itertools import cycle
from typing import Any, AsyncIterator, Callable, Coroutine, Iterator, List

import asynqp

from asynqp_consumer.helpers import gather
from asynqp_consumer.message import Message
from asynqp_consumer.records import ConnectionParams, Queue


logger = logging.getLogger(__name__)


class ConsumerCloseException(Exception):
    pass


class Consumer:

    RECONNECT_TIMEOUT = 3  # seconds

    def __init__(self,
                 queue: Queue,
                 callback: Callable[[List[Message]], Coroutine[Any, Any, None]],
                 connection_params: List[ConnectionParams] = None,
                 prefetch_count: int = 0,
                 check_bulk_interval: float = 0.3) -> None:
        self.queue: Queue = queue
        self.callback: Callable[[Any], Any] = callback
        self.connection_params = connection_params or [ConnectionParams()]
        self.prefetch_count = prefetch_count
        self.check_bulk_interval = check_bulk_interval

        self._connection_params_iterator: Iterator[ConnectionParams] = cycle(self.connection_params)
        self._connection: asynqp.Connection = None
        self._channel: asynqp.Channel = None
        self._queue: asynqp.Queue = None
        self._reconnect_attempts: int = 0
        self._messages: List[Message] = []
        self._messages_lock = asyncio.Lock()
        self._closed: asyncio.Future = None

    async def start(self, loop: asyncio.BaseEventLoop = None) -> None:
        assert not self._closed, 'Consumer already started.'

        self._closed = asyncio.Future()

        while not self._closed.done():
            try:
                await self._connect(loop=loop)

                await gather(
                    self._closed,
                    self._connection.closed,
                    self._process_queue(loop=loop),
                    self._check_bulk(loop=loop),
                    loop=loop
                )

            except (asynqp.AMQPConnectionError, OSError) as e:
                logger.exception(str(e))

                self._reconnect_attempts += 1
                timeout: int = self.RECONNECT_TIMEOUT * min(self._reconnect_attempts, 10)

                logger.info('Trying to recconnect in %d seconds.', timeout)

                await asyncio.sleep(timeout, loop=loop)

            except ConsumerCloseException:
                pass

        await self._disconnect()
        self._closed = None

    def close(self) -> None:
        self._closed.set_exception(ConsumerCloseException)

    async def _connect(self, loop: asyncio.BaseEventLoop) -> None:
        connection_params = next(self._connection_params_iterator)

        logger.info('Connection params: %s', connection_params)

        self._connection, self._channel = await asynqp.connect_and_open_channel(
            host=connection_params.host,
            port=connection_params.port,
            username=connection_params.username,
            password=connection_params.password,
            virtual_host=connection_params.virtual_host,
            loop=loop
        )

        logger.info('Connection and channel are ready.')

        await self._channel.set_qos(prefetch_count=self.prefetch_count)

        self._queue: asynqp.Queue = await self._channel.declare_queue(
            name=self.queue.name,
            durable=self.queue.durable,
            exclusive=self.queue.exclusive,
            auto_delete=self.queue.auto_delete,
            arguments=self.queue.arguments,
        )

        for binding in self.queue.bindings:
            exchange = await self._channel.declare_exchange(
                name=binding.exchange.name,
                type=binding.exchange.type,
                durable=binding.exchange.durable,
                auto_delete=binding.exchange.auto_delete,
                arguments=binding.exchange.arguments,
            )

            await self._queue.bind(
                exchange=exchange,
                routing_key=binding.routing_key,
                arguments=binding.arguments,
            )

        logger.info('Queue is ready.')

        self._reconnect_attempts = 0

    async def _disconnect(self) -> None:
        if self._channel:
            await self._channel.close()

        if self._connection:
            await self._connection.close()

    async def _process_queue(self, loop: asyncio.BaseEventLoop) -> None:
        self._messages = []
        async for message in self._iter_messages(loop=loop):
            try:
                wrapper = Message(message)
            except json.JSONDecodeError:
                logger.exception('Failed to parse message body: %s', message.body)
                message.reject(requeue=True)
                continue

            self._messages.append(wrapper)

            if self.prefetch_count != 0:
                await self._process_bulk()

    async def _iter_messages(self, loop: asyncio.BaseEventLoop) -> AsyncIterator[asynqp.IncomingMessage]:
        messages_queue = asyncio.Queue(loop=loop)

        await self._queue.consume(callback=messages_queue.put_nowait)

        while True:
            yield await messages_queue.get()

    async def _check_bulk(self, loop: asyncio.BaseEventLoop) -> None:
        while True:
            await asyncio.sleep(self.check_bulk_interval, loop=loop)
            await self._process_bulk(force=True)

    async def _process_bulk(self, force: bool = False) -> None:
        to_process: List[Message] = []

        with await self._messages_lock:
            count = self.prefetch_count if self.prefetch_count != 0 else len(self._messages)
            if force or len(self._messages) >= count:
                to_process = self._messages[:count]
                del self._messages[:count]

        if not to_process:
            return

        try:
            await self.callback(to_process)
        except Exception as e:  # pylint: disable=broad-except
            logger.exception(e)
            for message in to_process:
                message.reject()
        else:
            for message in to_process:
                message.ack()
