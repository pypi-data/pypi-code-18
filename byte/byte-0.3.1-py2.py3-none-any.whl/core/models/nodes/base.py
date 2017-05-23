"""byte - base nodes model module."""
from __future__ import absolute_import, division, print_function


class Node(object):
    """Node class."""

    def compile(self):
        """Compile node."""
        raise NotImplementedError('%s.compile() hasn\'t been implemented' % (self.__class__.__name__,))
