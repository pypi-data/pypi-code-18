from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.core.models.expressions.proxy import ProxyEqual, ProxyGreaterThanOrEqual, ProxyLessThan, ProxyNotEqual
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_simple():
    """Test select() query can be created with expressions."""
    query = users.select().where(
        User['id'] < 35,
        User['username'] != 'alpha'
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(2),
            has_items(
                # User['id'] < 35
                all_of(instance_of(ProxyLessThan), has_properties({
                    'lhs': User['id'],
                    'rhs': 35
                })),

                # User['username'] != 'alpha'
                all_of(instance_of(ProxyNotEqual), has_properties({
                    'lhs': User['username'],
                    'rhs': 'alpha'
                }))
            )
        )
    })))


def test_chain():
    """Test select() query can be created with chained expressions."""
    query = users.select().where(
        User['id'] >= 12
    ).where(
        User['username'] != 'beta'
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(2),
            has_items(
                # User['id'] >= 12
                all_of(instance_of(ProxyGreaterThanOrEqual), has_properties({
                    'lhs': User['id'],
                    'rhs': 12
                })),

                # User['username'] != 'beta'
                all_of(instance_of(ProxyNotEqual), has_properties({
                    'lhs': User['username'],
                    'rhs': 'beta'
                }))
            )
        )
    })))


def test_match():
    """Test select() query can be created with property matching expressions."""
    query = users.select().where(
        User['username'] == User['password']
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(1),
            has_items(
                # User['username'] == User['password']
                all_of(instance_of(ProxyEqual), has_properties({
                    'lhs': User['username'],
                    'rhs': User['password']
                }))
            )
        )
    })))
