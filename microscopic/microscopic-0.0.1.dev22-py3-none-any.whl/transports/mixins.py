import asyncio
from typing import Union


class StreamChunkMixin:
    async def read_chunk(self) -> bytes:
        try:
            data = await self.read_transport.readexactly(self.chunk_size)
        except asyncio.IncompleteReadError as ire:
            data = ire.partial
        return data

    async def write_chunk(self, data: Union[bytes, bytearray]):
        self.write_transport.write(data)
        await self.write_transport.drain()
