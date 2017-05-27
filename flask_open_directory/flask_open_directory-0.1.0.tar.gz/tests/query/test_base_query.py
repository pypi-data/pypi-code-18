import pytest
from flask_open_directory import BaseQuery, User
from flask_open_directory.query.base_query import _quote_if_str

import ldap3


@pytest.fixture
def base_query(open_directory):
    return BaseQuery(open_directory=open_directory)


@pytest.fixture
def connection():
    return ldap3.Connection(ldap3.Server('localhost'))


@pytest.fixture
def custom_model():

    class CustomModel(object):

        @classmethod
        def ldap_attribute_map(cls): pass

        @classmethod
        def attribute_name_for(cls, key): pass

        @classmethod
        def query_cn(cls):
            return 'cn=custom'

        @classmethod
        def from_entry(cls, entry): pass

        @classmethod
        def ldap_keys(cls): pass

    return CustomModel


def test_quote_if_str():
    assert _quote_if_str('a') == "'a'"
    assert _quote_if_str(None) is None
    obj = object()
    assert _quote_if_str(obj) == obj


def test_BaseQuery_model(base_query):
    base_query.model = User
    assert base_query.model == User

    base_query.model = User()
    assert base_query.model == User

    with pytest.raises(TypeError):
        base_query.model = object


def test_BaseQuery_open_directory(base_query):
    assert base_query.open_directory is not None

    with pytest.raises(TypeError):
        base_query.open_directory = object()


def test_BaseQuery_search_base(base_query, open_directory, custom_model):
    assert base_query.search_base == open_directory.base_dn
    base_query.model = User
    assert base_query.search_base == 'cn=users,' + open_directory.base_dn

    no_open_directory = BaseQuery()
    assert no_open_directory.search_base is None

    explicit = BaseQuery(search_base='dc=example,dc=com')
    assert explicit.search_base == 'dc=example,dc=com'

    custom = BaseQuery(open_directory=open_directory, model=custom_model)
    assert custom.model is not None
    assert custom.search_base == 'cn=custom,{}'.format(open_directory.base_dn)


def test_BaseQuery_search_filter(base_query):
    assert base_query.search_filter == base_query._default_search_filter
    q = BaseQuery(search_filter='(objectClass=apple-user)')
    assert q.search_filter == '(objectClass=apple-user)'


def test_BaseQuery_ldap_attributes(base_query):
    assert base_query.ldap_attributes is None
    base_query.ldap_attributes = ['a', 'b', object()]
    assert base_query.ldap_attributes == ('a', 'b')
    base_query.ldap_attributes = 'c'
    assert base_query.ldap_attributes == ('c', )


def test_BaseQuery_connection(base_query, connection):
    assert base_query.connection is None
    base_query.connection = connection
    assert base_query.connection == connection

    with pytest.raises(TypeError):
        base_query.connection = object()


def test_BaseQuery_connection_ctx(base_query, connection):

    with base_query.connection_ctx() as ctx:
        assert isinstance(ctx, ldap3.Connection)
        assert ctx != connection

    base_query.connection = connection
    with base_query.connection_ctx() as ctx:
        assert ctx == connection

    no_ctx = BaseQuery()
    with no_ctx.connection_ctx() as ctx:
        assert ctx is None


def test_BaseQuery_first(base_query, open_directory):
    base_query.model = User

    user = base_query.first()
    assert isinstance(user, User)

    entry = base_query.first(convert=False)
    assert isinstance(entry, ldap3.Entry)

    with base_query.connection_ctx() as conn:
        user = base_query.first(conn)
        assert isinstance(user, User)

    invalid = BaseQuery()
    item = invalid.first()
    assert item is None


def test_BaseQuery_all(base_query):
    base_query.model = User

    users = base_query.all()
    assert isinstance(users, tuple)
    for u in users:
        assert isinstance(u, User)

    entries = base_query.all(convert=False)
    for e in entries:
        assert isinstance(e, ldap3.Entry)

    with base_query.connection_ctx() as conn:
        users = base_query.all(conn)
        assert len(users) > 0

    invalid = BaseQuery()
    items = invalid.all()
    assert isinstance(items, tuple)
    assert len(items) == 0


def test_BaseQuery_repr(base_query, open_directory):
    r = repr(base_query)

    assert "model=None" in r
    assert "search_base='{}'".format(open_directory.base_dn) in r
    assert "search_filter='(objectClass=*)'" in r
    assert "open_directory={}".format(repr(open_directory)) in r
    assert "connection={}".format(base_query.connection) in r
    assert "ldap_attributes=None" in r
    assert "BaseQuery(" in r
    assert ")" in r
