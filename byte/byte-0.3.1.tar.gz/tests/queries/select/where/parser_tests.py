from __future__ import absolute_import, division, print_function

from byte.queries.where.parser import WHERE

from hamcrest import *


def test_and():
    """Test select() query can be created with AND string expression."""
    assert_that(WHERE.parseString('id < 35 AND username == "alpha"').asList(), equal_to([
        ['id', '<', '35'],
        'and',
        ['username', '==', '"alpha"']
    ]))


def test_brackets():
    """Test select() query can be created with brackets inside a string expression."""
    assert_that(WHERE.parseString('id < 35 AND (username == "alpha" OR username == "beta")').asList(), equal_to([
        ['id', '<', '35'],
        'and',
        [
            '(',
            ['username', '==', '"alpha"'],
            'or',
            ['username', '==', '"beta"'],
            ')'
        ]
    ]))


def test_or():
    """Test select() query can be created with OR string expression."""
    assert_that(WHERE.parseString('id < 35 OR username == "alpha"').asList(), equal_to([
        ['id', '<', '35'],
        'or',
        ['username', '==', '"alpha"']
    ]))


def test_parameters():
    """Test select() query can be created with parameters inside a string expression."""
    assert_that(WHERE.parseString('id < ? AND username == ?').asList(), equal_to([
        ['id', '<', '?'],
        'and',
        ['username', '==', '?']
    ]))


def test_simple():
    """Test select() query can be created with string expression."""
    assert_that(WHERE.parseString('id < 35').asList(), equal_to([
        ['id', '<', '35']
    ]))
