import asyncio
from collections import deque

from typing import AsyncGenerator, Callable, Deque, Union


Queue = Deque[Union[asyncio.Future, object]]
MatchProcessor = Callable[[memoryview], Union[bytes, bytearray]]


def unwrap(future):
    exc = future.exception()
    if exc:
        raise exc
    return future.result()


async def pump_queue(queue: Queue, *, wait: bool=False) -> AsyncGenerator[str, None]:
    while True:
        try:
            item = queue.popleft()
        except IndexError:
            break

        if not isinstance(item, asyncio.Future):
            yield item
        elif wait:
            await item
            yield unwrap(item)
        elif item.done():
            yield unwrap(item)
        else:
            queue.appendleft(item)
            break


def push_queue_pattern(strip: memoryview, match: memoryview, *,
                       queue: Queue, match_processor: MatchProcessor):
    #assert strip or match

    if strip:
        queue.append(strip)
    if match:
        queue.append(
            asyncio.ensure_future(
                match_processor(match)
            ))


class PatternQueueManager:
    def __init__(self, match_processor: MatchProcessor, queue_factory: Callable[[], Deque]=deque):
        self.queue = queue_factory()
        self.match_processor = match_processor

    def push(self, strip, match):
        push_queue_pattern(strip, match,
                           queue=self.queue, match_processor=self.match_processor)

    async def pump(self, wait: bool=False) -> memoryview:
        async for data in pump_queue(self.queue, wait=wait):
            yield data
