from functools import partial

from asynctest import mock
import pytest

from microscopic.pipelines import pipelines


class FakeAsyncContextManagerFactory:
    def __getattr__(self, name):
        return partial(FakeAsyncContextManager, name)


class FakeAsyncContextManager:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        return self.name

    async def __aexit__(self, *args):
        pass


@pytest.fixture
def context_factory():
    return FakeAsyncContextManagerFactory()


async def test_execute_simple(context_factory):
    pipeline = mock.CoroutineMock()

    await pipelines.execute_simple(
        pipeline,
        context_factory.read_transport,
        context_factory.write_transport,
        context_factory.processor,
        fake_arg='test'
    )

    pipeline.assert_called_once_with(
        'read_transport', 'write_transport', 'processor',
        fake_arg='test')
