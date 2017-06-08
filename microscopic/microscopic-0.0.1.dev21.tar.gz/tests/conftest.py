import asyncio
import inspect
from functools import wraps

import pytest


@pytest.fixture
def loop():
    return asyncio.get_event_loop()


def test(func):
    @wraps(func)
    def wrapper(**kwargs):
        __tracebackhide__ = True
        _loop = loop()
        return _loop.run_until_complete(func(**kwargs))
    return wrapper


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if inspect.iscoroutinefunction(pyfuncitem.obj):
        pyfuncitem.obj = test(pyfuncitem.obj)
