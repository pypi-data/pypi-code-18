import asyncio

from collections import deque
from unittest.mock import sentinel

import pytest

from microscopic import queue


async def match_processor(match):
    assert match == sentinel.match
    return sentinel.processed


@pytest.fixture
def queue_manager():
    return queue.PatternQueueManager(match_processor)


async def test_push_queue_pattern():
    dq = deque()

    queue.push_queue_pattern(sentinel.strip, sentinel.match,
                             queue=dq, match_processor=match_processor)

    assert dq.popleft() == sentinel.strip

    future = dq.popleft()
    assert isinstance(future, asyncio.Future)
    assert await future == sentinel.processed

    with pytest.raises(IndexError):
        dq.popleft()


@pytest.mark.skip(reason='not supported by pattern')
async def test_push_queue_assertion():
    dq = deque()

    with pytest.raises(AssertionError):
        queue.push_queue_pattern(None, None,
                                 queue=dq, match_processor=match_processor)


async def test_pattern_queue_manager(queue_manager):
    queue_manager.push(sentinel.strip, sentinel.match)

    expected = iter([sentinel.strip, sentinel.processed])

    async for data in queue_manager.pump(wait=True):
        assert data == next(expected)

    with pytest.raises(StopIteration):
        next(expected)
