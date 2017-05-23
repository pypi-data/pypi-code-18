"""byte - delete query module."""

from __future__ import absolute_import, division, print_function

from byte.queries.where import WhereQuery
from byte.queries.write import WriteQuery


class DeleteQuery(WhereQuery, WriteQuery):
    """Delete Query class."""

    pass
