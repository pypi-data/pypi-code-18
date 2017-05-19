"""byte - update query module."""

from __future__ import absolute_import, division, print_function

from byte.queries.where import WhereQuery
from byte.queries.write import WriteQuery


class UpdateQuery(WhereQuery, WriteQuery):
    """Update Query class."""

    def __init__(self, collection, model, data=None, state=None):
        """Create Update Query.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param data: Data
        :type data: dict or None

        :param state: Initial state
        :type state: dict or None
        """
        super(UpdateQuery, self).__init__(collection, model, state=state)

        self.data = data
