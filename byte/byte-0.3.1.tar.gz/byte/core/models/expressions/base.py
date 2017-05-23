"""byte - base expressions model module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.nodes import Node
from byte.core.models.property import BaseProperty


class Expressions(object):
    """Expressions class."""

    def and_(self, *values):
        """Create and expression."""
        raise NotImplementedError

    def asc(self):
        """Create ascending property definition."""
        raise NotImplementedError

    def between(self, low, high):
        """Create between expression."""
        raise NotImplementedError

    def bin_and(self, rhs):
        """Create binary and expression."""
        raise NotImplementedError

    def bin_or(self, rhs):
        """Create binary or expression."""
        raise NotImplementedError

    def concat(self, rhs):
        """Create concat expression."""
        raise NotImplementedError

    def contains(self, rhs):
        """Create contains expression."""
        raise NotImplementedError

    def desc(self):
        """Create descending property definition."""
        raise NotImplementedError

    def endswith(self, rhs):
        """Create ends-with expression."""
        raise NotImplementedError

    def in_(self, rhs):
        """Create in expression."""
        raise NotImplementedError

    def is_null(self, is_null=True):
        """Create is-null expression."""
        raise NotImplementedError

    def not_in(self, rhs):
        """Create not-in expression."""
        raise NotImplementedError

    def or_(self, *values):
        """Create or expression."""
        raise NotImplementedError

    def regexp(self, expression):
        """Create regexp expression."""
        raise NotImplementedError

    def startswith(self, rhs):
        """Create starts-with expression."""
        raise NotImplementedError

    def __and__(self, rhs):
        raise NotImplementedError

    def __eq__(self, rhs):
        raise NotImplementedError

    def __ge__(self, rhs):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __le__(self, rhs):
        raise NotImplementedError

    def __lshift__(self, rhs):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __mod__(self, other):
        raise NotImplementedError

    def __ne__(self, rhs):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __or__(self, rhs):
        raise NotImplementedError

    def __pos__(self):
        raise NotImplementedError

    def __pow__(self, rhs):
        raise NotImplementedError

    def __rand__(self, rhs):
        raise NotImplementedError

    def __ror__(self, rhs):
        raise NotImplementedError

    def __rshift__(self, rhs):
        raise NotImplementedError


class BaseExpression(Node, Expressions):
    """Base expression class."""

    def __init__(self, compiler):
        """Create expression.

        :param compiler: Compiler
        :type compiler: byte.compilers.core.base.Compiler
        """
        self._compiler = compiler

    @property
    def compiler(self):
        """Retrieve compiler.

        :rtype: byte.compilers.core.base.Compiler
        """
        return self._compiler


class Expression(BaseExpression):
    """Expression class."""

    def __init__(self, compiler, lhs, rhs):
        """Create expression.

        :param compiler: Compiler
        :type compiler: byte.compilers.core.base.Compiler

        :param lhs: Left Value
        :param rhs: Right Value
        """
        super(Expression, self).__init__(compiler)

        self.lhs = lhs
        self.rhs = rhs

    def resolve_lhs(self, item):
        """Resolve left value.

        :param item: Item
        """
        if isinstance(self.lhs, BaseProperty):
            return self.lhs.get(item)

        return self.lhs

    def resolve_rhs(self, item):
        """Resolve right value.

        :param item: Item
        """
        if isinstance(self.rhs, BaseProperty):
            return self.rhs.get(item)

        return self.rhs

    def execute(self, item):
        """Execute expression on item.

        :param item: Item

        :return: Result
        :rtype: bool
        """
        raise NotImplementedError('%s.execute() hasn\'t been implemented' % (self.__class__.__name__,))


class ManyExpression(BaseExpression):
    """Many expression class."""

    def __init__(self, compiler, *values):
        """Create many expression.

        :param compiler: Compiler
        :type compiler: byte.compilers.core.base.Compiler
        """
        super(ManyExpression, self).__init__(compiler)

        self.values = values


class StringExpression(Expression):
    """String expression class."""

    def __add__(self, other):
        return self.concat(other)

    def __radd__(self, other):
        return other.concat(self)


class And(ManyExpression):
    """And expression class."""

    pass


class Between(Expression):
    """Between expression class."""

    pass


class Equal(Expression):
    """Equal expression class."""

    def execute(self, item):
        """Execute equal expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) == self.resolve_rhs(item)


class GreaterThan(Expression):
    """Greater-than expression class."""

    def execute(self, item):
        """Execute greater-than expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) > self.resolve_rhs(item)


class GreaterThanOrEqual(Expression):
    """Greater-than-or-equal expression class."""

    def execute(self, item):
        """Execute greater-than-or-equal expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) >= self.resolve_rhs(item)


class In(Expression):
    """In expression class."""

    pass


class Is(Expression):
    """Is expression class."""

    pass


class IsNot(Expression):
    """Is-not expression class."""

    pass


class LessThan(Expression):
    """Less-than expression class."""

    def execute(self, item):
        """Execute less-than expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) < self.resolve_rhs(item)


class LessThanOrEqual(Expression):
    """Less-than-or-equal expression class."""

    def execute(self, item):
        """Execute less-than-or-equal expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) <= self.resolve_rhs(item)


class Like(Expression):
    """Like expression class."""

    pass


class NotEqual(Expression):
    """Not-equal expression class."""

    def execute(self, item):
        """Execute not-equal expression on item.

        :param item: Item
        """
        return self.resolve_lhs(item) != self.resolve_rhs(item)


class NotIn(Expression):
    """Not-in expression class."""

    pass


class Or(ManyExpression):
    """Or expression class."""

    pass


class RegularExpression(Expression):
    """Regular-expression class."""

    pass
