"""byte - select query module."""
from __future__ import absolute_import, division, print_function

from byte.core.helpers.object import clone
from byte.queries.where import WhereQuery

from six import string_types


class SelectQuery(WhereQuery):
    """Select Query class."""

    def __init__(self, collection, model, properties=None, state=None):
        """Create Select Query.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type model: byte.model.Model

        :param properties: Properties to select (or :code:`None` to select all properties)
        :type properties: tuple or None

        :param state: Initial state
        :type state: dict or None
        """
        super(SelectQuery, self).__init__(collection, model, state=state)

        # Update state
        self.state.setdefault('properties', properties)
        self.state.setdefault('from', [collection.parameters.get('table')])

        # Set defaults
        self.state.setdefault('distinct', False)

        self.state.setdefault('group_by', [])
        self.state.setdefault('order_by', [])

        self.state.setdefault('limit', None)
        self.state.setdefault('offset', None)

    @clone
    def distinct(self, on=True):
        """Enable distinct selection."""
        self.state['distinct'] = on

    @clone
    def group_by(self, *args, **kwargs):
        """Group results by properties."""
        raise NotImplementedError

    @clone
    def limit(self, count):
        """Set query limit."""
        self.state['limit'] = count

    @clone
    def offset(self, count):
        """Set query offset."""
        self.state['offset'] = count

    @clone
    def order_by(self, *properties):
        """Order results by :code:`properties`."""
        if 'order_by' not in self.state:
            self.state['order_by'] = []

        for prop in properties:
            prop, order, options = self._parse_order_property(prop)

            # Resolve `order` value
            if order:
                order = order.lower()

                if order.startswith('asc'):
                    order = 'ascending'
                elif order.startswith('desc'):
                    order = 'descending'

            # Build options dictionary
            if not options:
                options = {
                    'order': order or 'ascending'
                }

            # Resolve property key
            if isinstance(prop, string_types):
                prop = self.model.Internal.properties_by_key[prop]

            # Append property definition to state
            self.state['order_by'].append((prop, options))

    def count(self):
        """Execute query, and retrieve an integer representing the number of objects in the result."""
        return len(self.execute())

    def exists(self):
        """Execute query, and retrieve boolean indicating if any results were returned."""
        raise NotImplementedError

    def iterator(self):
        """Execute query, and retrieve the item iterator."""
        return iter(self.execute())

    def last(self):
        """Execute query, and retrieve the last item from the results."""
        raise NotImplementedError

    @staticmethod
    def _parse_order_property(prop):
        options = None
        order = None

        if type(prop) is not tuple:
            return prop, order, options

        if len(prop) != 2:
            raise ValueError('Invalid property definition')

        if type(prop[1]) is not dict and not isinstance(prop[1], string_types):
            raise ValueError('Invalid property definition')

        if isinstance(prop[1], string_types):
            prop, order = prop
        else:
            prop, options = prop

        return prop, order, options

    def __iter__(self):
        return self.iterator()
