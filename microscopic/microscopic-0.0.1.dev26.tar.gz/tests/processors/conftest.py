from unittest.mock import patch

from aiohttp.test_utils import RawTestServer, TestClient
import pytest
from yarl import URL


def make_url(self, path):
    url = URL(path).relative()
    return self._root.join(url)


@pytest.fixture
def test_client(loop):
    clients = []

    async def go(__param, **kwargs):
        client = TestClient(__param, loop=loop, **kwargs)

        await client.start_server()
        clients.append(client)
        return client

    yield go

    async def finalize():
        while clients:
            await clients.pop().close()

    loop.run_until_complete(finalize())


@pytest.fixture
def test_server(loop):
    servers = []

    async def go(handler, **kwargs):
        server = RawTestServer(handler)
        await server.start_server(loop=loop, **kwargs)
        servers.append(server)
        return server

    with patch.object(RawTestServer, 'make_url', new=make_url):
        yield go

    async def finalize():
        while servers:
            await servers.pop().close()

    loop.run_until_complete(finalize())
