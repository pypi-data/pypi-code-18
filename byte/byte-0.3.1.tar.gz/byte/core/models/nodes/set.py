"""byte - node set module."""
from __future__ import absolute_import, division, print_function

from byte.core.models.nodes.base import Node


class Set(Node):
    """Node set class."""

    def __init__(self, *nodes, **kwargs):
        """Create node set.

        :param nodes: Nodes
        :type nodes: list of Node

        :param kwargs Options (overrides defaults)
        :type kwargs: dict
        """
        self.nodes = list(nodes)
