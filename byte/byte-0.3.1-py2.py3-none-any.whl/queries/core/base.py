"""byte - query base module."""

from __future__ import absolute_import, division, print_function


class Query(object):
    """Query class."""

    def __init__(self, collection, model, state=None):
        """Create Query.

        :param collection: Collection
        :type collection: byte.collection.Collection

        :param model: Model
        :type: model: class

        :param state: Initial state
        :type state: dict or None
        """
        self.collection = collection
        self.model = model

        self.state = state or {}

        self._result = None

    def clone(self):
        """Clone Query.

        :return: Query
        :rtype: Query
        """
        def copy(value):
            if type(value) is dict:
                return value.copy()

            if type(value) is list:
                return list(value)

            if type(value) is tuple:
                return tuple(value)

            return value

        return self.__class__(
            self.collection, self.model,
            state=copy(self.state)
        )

    def execute(self):
        """Execute query."""
        return self.collection.execute(self)

    def filter(self, *args, **kwargs):
        """Filter query results."""
        raise NotImplementedError

    def first(self):
        """Execute query, and return the first item from the result."""
        with self.execute() as result:
            for item in result:
                return item

        return None

    def __enter__(self):
        self._result = self.execute()

        return self._result

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._result is None:
            return

        self._result.close()
