import os

import pytest

from microscopic.transports import pipe


class Pipe:
    master = None
    fd = None


@pytest.fixture
def read_pipe():
    slave, master = os.pipe()
    pipe = Pipe()
    pipe.fd = slave
    pipe.master = os.fdopen(master, 'wb', 0)
    return pipe


@pytest.fixture
def write_pipe():
    master, slave = os.pipe()
    pipe = Pipe()
    pipe.fd = slave
    pipe.master = os.fdopen(master, 'rb', 0)
    return pipe


@pytest.fixture
def pt(read_pipe, write_pipe):
    return pipe.PipeTransport(
        read_pipe.fd, write_pipe.fd,
        chunk_size=1
    )


async def test_read_sanity(pt, read_pipe):
    read_pipe.master.write(b't')

    async with pt:
        result = await pt.read_chunk()

    assert result == b't'


async def test_write_sanity(pt, write_pipe):
    async with pt:
        await pt.write_chunk(b't')

    result = write_pipe.master.read()
    assert result == b't'


async def test_context_manager_returns_self(pt):
    async with pt as pt:
        assert isinstance(pt, pipe.PipeTransport)


async def test_context_manager_closes(pt, write_pipe, read_pipe):
    async with pt:
        pass

    with pytest.raises(BrokenPipeError):
        read_pipe.master.write(b't')

    assert write_pipe.master.read(1) == b''
