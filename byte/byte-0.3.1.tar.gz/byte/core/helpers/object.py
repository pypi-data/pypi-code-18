"""byte - object helper functions."""
from __future__ import absolute_import, division, print_function

import functools


def clone(func):
    """Clone object decorator."""
    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        if not hasattr(self, 'clone'):
            raise ValueError('%s has no "clone" method defined' % (self.__class__.__name__,))

        # Clone existing query
        query = self.clone()

        # Execute operation, and return new query
        func(query, *args, **kwargs)
        return query

    return inner
