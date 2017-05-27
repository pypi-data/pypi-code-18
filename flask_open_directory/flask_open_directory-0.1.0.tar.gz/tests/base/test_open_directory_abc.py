import pytest
from contextlib import contextmanager
from flask_open_directory import OpenDirectoryABC


@pytest.fixture
def valid_object():

    class Valid(object):

        @property
        def server_url(self): pass

        @property
        def base_dn(self): pass

        @property
        def connection(self): pass

        @contextmanager
        def connection_ctx(self): pass

    return Valid


def test_OpenDirectoryABC(valid_object):

    assert issubclass(valid_object, OpenDirectoryABC)
    assert isinstance(valid_object(), OpenDirectoryABC)


def test_invalid_OpenDirectoryABC(valid_object):

    del(valid_object.server_url)
    assert issubclass(valid_object, OpenDirectoryABC) is False
    assert isinstance(valid_object(), OpenDirectoryABC) is False
