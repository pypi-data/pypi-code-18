import asyncio
import os

from microscopic.transports import mixins


class PipeTransport(mixins.StreamChunkMixin):
    def __init__(self, read_fd: int, write_fd: int, *, chunk_size: int):
        self._read_pipe = os.fdopen(read_fd, 'rb', 0)
        self._write_pipe = os.fdopen(write_fd, 'wb', 0)

        self.chunk_size = chunk_size

    async def __aenter__(self):
        assert (not hasattr(self, 'read_transport') and
                not hasattr(self, 'write_transport'))

        loop = asyncio.get_event_loop()

        reader = asyncio.StreamReader(limit=self.chunk_size)

        transport, _ = await loop.connect_read_pipe(
            lambda: asyncio.StreamReaderProtocol(reader),
            self._read_pipe)

        transport, protocol = await loop.connect_write_pipe(
            asyncio.streams.FlowControlMixin,
            self._write_pipe)

        writer = asyncio.StreamWriter(transport, protocol, reader, loop)

        self.read_transport = reader
        self.write_transport = writer

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._read_pipe.close()
        self._write_pipe.close()
