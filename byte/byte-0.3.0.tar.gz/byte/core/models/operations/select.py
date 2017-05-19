"""byte - compiler select operation module."""

from __future__ import absolute_import, division, print_function

from byte.core.models.operations.base import Operation


class SelectOperation(Operation):
    """Select operation class."""

    def __init__(self, where):
        """Create select operation.

        :param where: Where expressions
        :type where: list
        """
        self.where = where
