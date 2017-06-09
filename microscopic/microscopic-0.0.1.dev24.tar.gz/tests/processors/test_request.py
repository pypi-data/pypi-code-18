from unittest.mock import sentinel

from aiohttp import web
import pytest

from microscopic.processors import request


async def request_factory(session, data):
    assert not session.closed
    assert data == sentinel.data
    return sentinel.response


@pytest.fixture
def rp():
    return lambda: request.RequestProcessor(request_factory)


async def test_request_processor(rp):
    async with rp() as rp:
        result = await rp(sentinel.data)

    assert result == sentinel.response


async def test_request_processor_closes_session(rp):
    async with rp() as rp:
        pass

    with pytest.raises(AssertionError):
        await rp(sentinel.data)


async def test_short_url_factory(test_client, test_server):
    async def handler(request):
        data = await request.json()
        assert data['content'] == 'request'
        return web.json_response({'url': 'response'})

    server = await test_server(handler)
    client = await test_client(server)

    result = await request.short_url_factory(client, b'request')
    assert result == b'response'
