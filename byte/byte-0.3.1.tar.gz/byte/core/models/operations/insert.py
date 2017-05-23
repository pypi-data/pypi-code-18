"""byte - compiler insert operation module."""

from __future__ import absolute_import, division, print_function

from byte.core.models.operations.base import Operation


class InsertOperation(Operation):
    """Insert operation class."""

    def __init__(self, items):
        """Create insert operation.

        :param items: Items to insert
        :type items: list of dict
        """
        self.items = items
