from __future__ import absolute_import, division, print_function

from byte.collection import Collection
from byte.core.models.expressions.proxy import ProxyEqual, ProxyLessThan, ProxyNotEqual, ProxyOr
from tests.base.models.dynamic.user import User

from hamcrest import *

users = Collection(User)


def test_or():
    """Test select() query can be created with an OR operator inside a string expression."""
    query = users.select().where(
        'id < 35 or username == "alpha"'
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(1),
            has_items(
                # id < 35 or username == "alpha"
                all_of(instance_of(ProxyOr), has_properties({
                    'values': all_of(
                        has_length(2),
                        has_items(
                            # id < 35
                            all_of(instance_of(ProxyLessThan), has_properties({
                                'lhs': User['id'],
                                'rhs': 35
                            })),

                            # username == "alpha"
                            all_of(instance_of(ProxyEqual), has_properties({
                                'lhs': User['username'],
                                'rhs': 'alpha'
                            }))
                        )
                    )
                }))
            )
        )
    })))


def test_or_brackets():
    """Test select() query can be created with an OR operator and brackets inside a string expression."""
    query = users.select().where(
        'id < 35 AND (username != "alpha" or password == "beta") AND password ne "alpha"'
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(3),
            has_items(
                # id < 35
                all_of(instance_of(ProxyLessThan), has_properties({
                    'lhs': User['id'],
                    'rhs': 35
                })),

                # (username != "alpha" or password == "beta")
                all_of(instance_of(ProxyOr), has_properties({
                    'values': all_of(
                        has_length(2),
                        has_items(
                            # username != "alpha"
                            all_of(instance_of(ProxyNotEqual), has_properties({
                                'lhs': User['username'],
                                'rhs': 'alpha'
                            })),

                            # password == "beta"
                            all_of(instance_of(ProxyEqual), has_properties({
                                'lhs': User['password'],
                                'rhs': 'beta'
                            }))
                        )
                    )
                })),

                # password ne "alpha"
                all_of(instance_of(ProxyNotEqual), has_properties({
                    'lhs': User['password'],
                    'rhs': 'alpha'
                }))
            )
        )
    })))


def test_parameters():
    """Test select() query can be created with parameters inside a string expression."""
    query = users.select().where(
        'id < ? AND username != ?',
        (35, 'alpha')
    )

    assert_that(query, has_property('state', has_entries({
        # where()
        'where': all_of(
            has_length(2),
            has_items(
                # id < 35
                all_of(instance_of(ProxyLessThan), has_properties({
                    'lhs': User['id'],
                    'rhs': 35
                })),

                # username == "alpha"
                all_of(instance_of(ProxyNotEqual), has_properties({
                    'lhs': User['username'],
                    'rhs': 'alpha'
                }))
            )
        )
    })))
