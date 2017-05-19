"""byte - proxy expressions module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.expressions.base import (
    BaseExpression,
    Expressions,
    Expression,
    ManyExpression,
    StringExpression,

    And,
    Between,
    Equal,
    GreaterThan,
    GreaterThanOrEqual,
    In,
    Is,
    IsNot,
    LessThan,
    LessThanOrEqual,
    Like,
    NotEqual,
    NotIn,
    Or,
    RegularExpression
)


class ProxyExpressions(Expressions):
    """Proxy expression class."""

    def and_(self, *values):
        """Create and proxy expression."""
        return ProxyAnd(self, *values)

    def or_(self, *values):
        """Create or proxy expression."""
        return ProxyOr(self, *values)

    def __and__(self, rhs):
        return ProxyAnd(self, rhs)

    def __eq__(self, rhs):
        if rhs is None:
            return ProxyIs(self, rhs)

        return ProxyEqual(self, rhs)

    def __ge__(self, rhs):
        return ProxyGreaterThanOrEqual(self, rhs)

    def __gt__(self, rhs):
        return ProxyGreaterThan(self, rhs)

    def __le__(self, rhs):
        return ProxyLessThanOrEqual(self, rhs)

    def __lt__(self, rhs):
        return ProxyLessThan(self, rhs)

    def __ne__(self, rhs):
        if rhs is None:
            return ProxyIsNot(self, rhs)

        return ProxyNotEqual(self, rhs)

    def __or__(self, rhs):
        return ProxyOr(self, rhs)


class BaseProxyExpression(BaseExpression):
    """Base proxy expression class."""

    pass


class ProxyExpression(Expression, ProxyExpressions, BaseProxyExpression):
    """Proxy expression class."""

    def __init__(self, lhs, rhs):
        """Create proxy expression.

        :param lhs: Left Value
        :param rhs: Right Value
        """
        super(ProxyExpression, self).__init__(None, lhs, rhs)


class ProxyManyExpression(ManyExpression, ProxyExpressions, BaseProxyExpression):
    """Proxy many expression class."""

    def __init__(self, *values):
        """Create proxy many expression."""
        super(ProxyManyExpression, self).__init__(None, *values)


class ProxyStringExpression(StringExpression, ProxyExpressions, BaseProxyExpression):
    """Proxy string expression class."""

    def __init__(self, lhs, rhs):
        """Create proxy string expression.

        :param lhs: Left Value
        :param rhs: Right Value
        """
        super(ProxyStringExpression, self).__init__(None, lhs, rhs)


class ProxyAnd(And, ProxyManyExpression):
    """Proxy and expression class."""

    pass


class ProxyBetween(Between, ProxyExpression):
    """Proxy between expression class."""

    pass


class ProxyEqual(Equal, ProxyExpression):
    """Proxy equal expression class."""

    pass


class ProxyGreaterThan(GreaterThan, ProxyExpression):
    """Proxy greater-than expression class."""

    pass


class ProxyGreaterThanOrEqual(GreaterThanOrEqual, ProxyExpression):
    """Proxy greater-than-or-equal expression class."""

    pass


class ProxyIn(In, ProxyExpression):
    """Proxy in expression class."""

    pass


class ProxyIs(Is, ProxyExpression):
    """Proxy is expression class."""

    pass


class ProxyIsNot(IsNot, ProxyExpression):
    """Proxy is-not expression class."""

    pass


class ProxyLessThan(LessThan, ProxyExpression):
    """Proxy less-than expression class."""

    pass


class ProxyLessThanOrEqual(LessThanOrEqual, ProxyExpression):
    """Proxy less-than-or-equal expression class."""

    pass


class ProxyLike(Like, ProxyExpression):
    """Proxy like expression class."""

    pass


class ProxyNotEqual(NotEqual, ProxyExpression):
    """Proxy not-equal expression class."""

    pass


class ProxyNotIn(NotIn, ProxyExpression):
    """Proxy not-in expression class."""

    pass


class ProxyOr(Or, ProxyManyExpression):
    """Proxy or expression class."""

    pass


class ProxyRegularExpression(RegularExpression, ProxyExpression):
    """Proxy regular-expression class."""

    pass
