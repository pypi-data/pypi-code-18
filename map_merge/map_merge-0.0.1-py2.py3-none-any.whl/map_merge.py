"""
    map_merge
    ~~~~~~~~~

    Contains functionality for merging Python mapping instances.
"""
from __future__ import unicode_literals

import collections
import six


__all__ = ['merge', 'merge_objects']


def merge(maps, mutate=True):
    """
    Merge the sequence of :class:`~collections.Mapping` objects together.

    :param maps: A sequence of mapping instance to merge.
    :param mutate: Optional flag indicating if a new map should be created or merged into the first.
    :return: All mapping instances merged together.
    """
    if not maps:
        raise ValueError('Must provide at least once mapping to merge')

    merged = maps.pop(0) if mutate else {}

    for map in maps:
        merged = merge_objects(merged, map)

    return merged


def merge_objects(lhs, rhs):
    """
    Merge two objects together, if possible, with the "right hand side" taking precedence on conflicts.

    If a merge is not possible, a :class:`TypeError` is raised.

    :param lhs: Object that the "right hand side" should be merged into.
    :param rhs: Object that should be merged into the "left hand side".
    :return: Two objects merged together.
    """
    if isinstance(lhs, (six.integer_types, float, six.string_types, type(None))):
        return rhs

    if isinstance(lhs, collections.MutableSequence):
        lhs.extend(rhs) if isinstance(rhs, collections.Sequence) else lhs.append(rhs)
        return lhs

    if isinstance(lhs, collections.Set):
        return lhs.union(rhs)

    if isinstance(lhs, collections.MutableMapping) and isinstance(rhs, collections.MutableMapping):
        for key in rhs:
            lhs[key] = merge_objects(lhs.get(key), rhs[key])
        return lhs

    raise TypeError('Cannot merge type {} into type {}'.format(rhs.__class__.__name__, lhs.__class__.__name__))
