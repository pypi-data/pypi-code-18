import asyncio
from typing import Sequence

from microscopic.transports import mixins


class SubprocessTransport(mixins.StreamChunkMixin):
    def __init__(self, *args: Sequence, chunk_size: int, **kwargs):
        coro = asyncio.create_subprocess_exec(
            *args,
            limit=chunk_size,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            **kwargs,
        )
        self._process = asyncio.ensure_future(coro)

        self.chunk_size = chunk_size

    async def __aenter__(self):
        assert not isinstance(self._process, asyncio.subprocess.Process)

        self._process = await self._process
        self.read_transport = self._process.stdout
        self.write_transport = self._process.stdin

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        assert isinstance(self._process, asyncio.subprocess.Process)

        self._process.stdin.close()
        await self._process.wait()
