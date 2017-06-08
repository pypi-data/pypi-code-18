import asyncio

from typing import AsyncGenerator, Deque, Union


async def pump_queue(queue: Deque[Union[asyncio.Future, str]], *, wait: bool=False) -> AsyncGenerator[str, None]:
    while True:
        try:
            item = queue.popleft()
        except IndexError:
            break

        if isinstance(item, str):
            yield item
        elif item.done():
            yield item.result()
        elif wait:
            yield await item
        else:
            queue.appendleft(item)
            break
