import pytest

from flask_open_directory.model import User, Group
from flask_open_directory.query import Query


@pytest.fixture
def user_query(open_directory):
    return Query(open_directory, model=User)


def test_Query_filter(user_query):

    assert user_query.search_filter == user_query._default_search_filter

    user_query.filter('(uid=testuser)')
    assert user_query.search_filter == '(uid=testuser)'

    user_query.filter(full_name='Test User')
    print(User.attribute_for_key('full_name'))
    assert user_query.search_filter == '(cn=Test User)'


def test_Query_filter_multiple_kwargs(user_query):
    assert user_query.search_filter == user_query._default_search_filter
    user_query.filter(username='testuser', cn='Test User')
    assert user_query.search_filter == '(&(uid=testuser)(cn=Test User))'


def test_Query_filter_is_chainable(user_query):
    assert user_query.filter(uid='testuser') == user_query


def test_calling_an_instance_updates_model(user_query):
    assert user_query.model == User
    user_query(Group)
    assert user_query.model == Group


def test_calling_an_instance_is_chainable(user_query):
    assert user_query(Group) == user_query
