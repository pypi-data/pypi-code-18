"""byte - insert query module."""
from __future__ import absolute_import, division, print_function

from byte.core.helpers.object import clone
from byte.queries.write import WriteQuery


class InsertQuery(WriteQuery):
    """Insert Query class."""

    def __init__(self, collection, model, items=None, properties=None, query=None, state=None):
        """Create Insert Query.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param items: Items to insert
        :type items: list or None

        :param query: Insertion query
        :type query: object

        :param state: Initial state
        :type state: dict or None
        """
        super(InsertQuery, self).__init__(collection, model, state=state)

        if items is None:
            items = []

        if properties is None:
            properties = model.Internal.properties_by_name.values()

        # Update state
        self.state.setdefault('items', items)
        self.state.setdefault('properties', properties)
        self.state.setdefault('query', query)

    @clone
    def items(self, *args, **kwargs):
        """Append items to insert query."""
        for value in args:
            if isinstance(value, (list, tuple)):
                self.state['items'].extend(value)
            elif isinstance(value, dict):
                self.state['items'].append(value)
            else:
                raise ValueError('Unsupported item value type: %s' % (type(value).__name__,))

        if kwargs:
            self.state['items'].append(kwargs)

    def upsert(self):
        """Update item, or insert if it doesn't exist."""
        raise NotImplementedError
