import asyncio

from typing import AsyncGenerator, Deque, Union


def unwrap(future):
    exc = future.exception()
    if exc:
        raise exc
    return future.result()


async def pump_queue(queue: Deque[Union[asyncio.Future, str]], *, wait: bool=False) -> AsyncGenerator[str, None]:
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
