import pytest
from flask_open_directory.model.model_abc import ModelABC


@pytest.fixture
def valid_object():

    class Valid(object):

        @classmethod
        def ldap_attribute_map(cls): pass

        @classmethod
        def attribute_name_for(cls, key): pass

        @classmethod
        def query_cn(cls): pass

        @classmethod
        def from_entry(cls, entry): pass

        @classmethod
        def ldap_keys(cls): pass

    return Valid


def test_valid(valid_object):

    assert issubclass(valid_object, ModelABC)
    assert isinstance(valid_object(), ModelABC)


def test_invalid(valid_object):

    del(valid_object.ldap_keys)
    assert issubclass(valid_object, ModelABC) is False
    assert isinstance(valid_object(), ModelABC) is False
