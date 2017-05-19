"""byte - where query module."""

from __future__ import absolute_import, division, print_function

from byte.core.helpers.object import clone
from byte.core.models.expressions.base import BaseExpression
from byte.core.models.expressions.proxy import (
    ProxyAnd,
    ProxyEqual,
    ProxyGreaterThan,
    ProxyGreaterThanOrEqual,
    ProxyLessThan,
    ProxyLessThanOrEqual,
    ProxyNotEqual,
    ProxyOr
)
from byte.queries.core.base import Query
from byte.queries.where.parser import WHERE

from six import string_types


class WhereQuery(Query):
    """Where Query class."""

    def __init__(self, collection, model, state=None):
        """Create where query.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param state: Initial state
        :type state: dict or Noen
        """
        super(WhereQuery, self).__init__(collection, model, state=state)

        # Set defaults
        self.state.setdefault('where', [])

    @clone
    def where(self, *args):
        """Retrieve items matching expressions (args)."""
        if not args:
            return

        if 'where' not in self.state:
            self.state['where'] = []

        # Parse string, and append expressions to state
        if isinstance(args[0], string_types):
            self.state['where'].extend(self.__parse_string(*args))
            return

        # Append expressions to state
        for value in args:
            self.state['where'].append(value)

    def __parse_string(self, value, *parameters):
        if not value:
            return []

        if len(parameters) == 1 and type(parameters[0]) is tuple:
            parameters = parameters[0]

        # Parse expressions from string
        offset, expression = self.__parse_string_parts(
            WHERE.parseString(value).asList(),
            parameters=parameters
        )

        if (offset or parameters) and offset != len(parameters):
            raise Exception('Found %d parameter token(s), but only %d value(s) were provided' % (
                offset, len(parameters)
            ))

        if isinstance(expression, ProxyAnd):
            return expression.values

        return [expression]

    def __parse_string_parts(self, parts, offset=0, parameters=None):
        if (len(parts) - 1) % 2 > 0:
            raise ValueError('Incorrect number of expression parts')

        if parts[0] == '(' and parts[-1] == ')':
            parts = parts[1:-1]

        expressions = []
        pos = 0

        while pos < len(parts):
            # Retrieve left value
            if expressions:
                left = expressions[-1]
            else:
                left = parts[pos]
                pos += 1

            # Retrieve operator and right value
            op = parts[pos]
            right = parts[pos + 1]
            pos += 2

            # Resolve values
            offset, left = self.__resolve_string_value(
                left,
                offset=offset,
                parameters=parameters
            )

            offset, right = self.__resolve_string_value(
                right,
                offset=offset,
                parameters=parameters
            )

            # Append expression
            expression = self.__construct_expression(expressions, op, left, right)

            if expression:
                expressions.append(expression)

        if len(expressions) == 1:
            return offset, expressions[0]

        return offset, ProxyAnd(*expressions)

    def __resolve_string_value(self, value, offset=0, parameters=None):
        if isinstance(value, BaseExpression):
            return offset, value

        if isinstance(value, list):
            return self.__parse_string_parts(
                value,
                offset=offset,
                parameters=parameters
            )

        # String
        if value == '?':
            if offset < len(parameters):
                return offset + 1, parameters[offset]

            return offset + 1, '?'

        if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
            return offset, value[1:-1]

        # Integer
        try:
            return offset, int(value)
        except (TypeError, ValueError):
            pass

        # Column
        return offset, self.model.Internal.properties_by_name[value]

    def __construct_expression(self, expressions, op, left, right):
        if op in ['eq', '=', '==']:
            return ProxyEqual(left, right)

        if op in ['ne', '!=']:
            return ProxyNotEqual(left, right)

        if op in ['lt', '<']:
            return ProxyLessThan(left, right)

        if op in ['le', '<=']:
            return ProxyLessThanOrEqual(left, right)

        if op in ['gt', '>']:
            return ProxyGreaterThan(left, right)

        if op in ['ge', '>=']:
            return ProxyGreaterThanOrEqual(left, right)

        if op == 'and':
            if not expressions:
                expressions.append(left)

            expressions.append(right)
            return None

        if op == 'or':
            return ProxyOr(left, right)

        raise NotImplementedError
