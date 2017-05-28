import pytest
from flask_open_directory.query import QueryABC


@pytest.fixture
def valid_object():

    class Valid(object):

        @property
        def search_base(self): pass

        @property
        def search_filter(self): pass

        @property
        def connection(self): pass

        @property
        def ldap_attributes(self): pass

        def all(self, connection=None): pass

        def first(self, connection=None): pass

    return Valid


@pytest.fixture
def invalid_object():

    class Invalid(object):
        pass

    return Invalid


def test_QueryABC(valid_object, invalid_object):

    assert issubclass(valid_object, QueryABC)
    assert isinstance(valid_object(), QueryABC)

    assert issubclass(invalid_object, QueryABC) is False
    assert isinstance(invalid_object(), QueryABC) is False
