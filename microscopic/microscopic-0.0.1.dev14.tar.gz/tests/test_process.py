import asyncio
from collections import deque

import pytest

from microscopic import process


async def as_list(gen, l=None):
    l = [] if l is None else l

    async for item in gen:
        l.append(item)

    return l


async def test_pump_queue_empty_queue(loop):
    queue = deque([])

    result = await as_list(process.pump_queue(queue))

    assert result == []


async def test_pump_queue_strings(loop):
    expected = ['foo', 'bar']
    queue = deque(expected)

    result = await as_list(process.pump_queue(queue))

    assert result == expected


async def test_pump_queue_string_future(loop):
    future = loop.create_future()
    queue = deque(['foo', future, 'bar'])

    result = await as_list(process.pump_queue(queue))
    assert result == ['foo']

    future.set_result('test')
    result = await as_list(process.pump_queue(queue))
    assert result == ['test', 'bar']


async def test_pump_queue_string_future_wait(loop):
    future = loop.create_future()
    queue = deque(['foo', future, 'bar'])

    result = []
    with pytest.raises(asyncio.TimeoutError):
        coro = as_list(process.pump_queue(queue, wait=True), result)
        await asyncio.wait_for(coro, 0)

    assert result == ['foo']
    assert future.cancelled()
