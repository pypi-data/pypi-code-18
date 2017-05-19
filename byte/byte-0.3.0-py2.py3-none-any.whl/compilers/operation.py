"""byte - operation compiler module."""

from __future__ import absolute_import, division, print_function

from byte.compilers.core.base import CompilerPlugin
from byte.core.models import InsertOperation, SelectOperation
from byte.queries import InsertQuery, SelectQuery


class OperationCompiler(CompilerPlugin):
    """Operation compiler class."""

    key = 'operation'

    def compile(self, query):
        """Compile query.

        :param query: Query
        :type query: byte.queries.Query

        :return: Operation
        :rtype byte.core.models.Operation
        """
        if isinstance(query, InsertQuery):
            return self.compile_insert(query)

        if isinstance(query, SelectQuery):
            return self.compile_select(query)

        raise NotImplementedError('Unsupported query: %s' % (query,))

    def compile_insert(self, query):
        """Compile insert query.

        :param query: Insert Query
        :type query: byte.queries.InsertQuery

        :return: Insert Operation
        :rtype byte.core.models.InsertOperation
        """
        if query.state['query']:
            raise NotImplementedError('"query" is not supported on insert queries')

        return InsertOperation(
            items=query.state['items']
        )

    def compile_select(self, query):
        """Compile select query.

        :param query: Select Query
        :type query: byte.queries.SelectQuery

        :return: Select Operation
        :rtype byte.core.models.SelectOperation
        """
        return SelectOperation(
            where=query.state['where']
        )
