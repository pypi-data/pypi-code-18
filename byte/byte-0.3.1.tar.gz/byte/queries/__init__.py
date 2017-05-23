"""byte - queries package."""

from __future__ import absolute_import, division, print_function

from byte.queries.core.base import Query
from byte.queries.delete import DeleteQuery
from byte.queries.insert import InsertQuery
from byte.queries.select import SelectQuery
from byte.queries.update import UpdateQuery

__all__ = (
    'Query',
    'DeleteQuery',
    'InsertQuery',
    'SelectQuery',
    'UpdateQuery'
)
