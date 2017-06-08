import asyncio
from unittest.mock import sentinel

from asynctest import mock
import pytest

from microscopic.transports import mixins


@pytest.fixture
def mock_transport():
    return mock.CoroutineMock()


@pytest.fixture
def scm(mock_transport):
    scm = mixins.StreamChunkMixin()
    scm.read_transport = mock_transport
    scm.write_transport = mock_transport
    scm.chunk_size = sentinel.chunk_size
    return scm


async def test_scm_write_chunk(scm, mock_transport):
    await scm.write_chunk(b'test')

    mock_transport.write.assert_called_once_with(b'test')
    mock_transport.drain.assert_called_once()


async def test_scm_read_chunk(scm, mock_transport):
    mock_transport.readexactly.return_value = b'test'

    result = await scm.read_chunk()

    mock_transport.readexactly.assert_called_once_with(sentinel.chunk_size)
    assert result == b'test'


async def test_scm_read_chunk_ire(scm, mock_transport):
    exc = asyncio.IncompleteReadError(b'partial', 0)
    mock_transport.readexactly.side_effect = exc

    result = await scm.read_chunk()

    assert result == b'partial'
