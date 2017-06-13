from functools import reduce
from operator import getitem
from typing import Any, Callable, Sequence, Tuple

from basic_utils.seq_helpers import butlast, last

__all__ = [
    'dict_subset',
    'get_in_dict',
    'get_keys',
    'prune_dict',
    'set_in_dict',
]


def get_keys(d: dict, keys: Sequence[Any], default: Callable=None) -> Tuple:
    """
    Returns multiple values for keys in a dictionary

    Empty key values will be None by default

    >>> d = {'x': 24, 'y': 25}
    >>> get_keys(d, ('x', 'y', 'z'))
    (24, 25, None)
    """
    return tuple(d.get(key, default) for key in keys)


def dict_subset(d, keys, prune=False, default=None):
    # type: (dict, Sequence[str], bool, Callable) -> dict
    """
    Returns a new dictionary with a subset of key value pairs from the original

    >>> d = {'a': 1, 'b': 2}
    >>> dict_subset(d, ('c',), True, 'missing')
    {'c': 'missing'}
    """
    new = {k: d.get(k, default) for k in keys}
    if prune:
        return prune_dict(new)
    return new


def get_in_dict(d: dict, keys: Sequence[str]) -> Any:
    """
    Retrieve nested key from dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> get_in_dict(d, ('a', 'b', 'c'))
    3
    """
    return reduce(getitem, keys, d)


def set_in_dict(d: dict, keys: Sequence[str], value: Any) -> None:
    """
    Sets a value inside a nested dictionary

    >>> d = {'a': {'b': {'c': 3}}}
    >>> set_in_dict(d, ('a', 'b', 'c'), 10)
    >>> d
    {'a': {'b': {'c': 10}}}
    """
    get_in_dict(d, butlast(keys))[last(keys)] = value


def prune_dict(d: dict) -> dict:
    """
    Returns new dictionary with falesly values removed.

    >>> prune_dict({'a': [], 'b': 2, 'c': False})
    {'b': 2}
    """
    return filter_values(d, lambda x: bool(x))


def filter_keys(d: dict, predicate: Callable) -> dict:
    """
    Returns new subset dict of d where keys pass predicate fn

    >>> filter_keys({'Lisa': 8, 'Marge': 36}, lambda x: len(x) > 4)
    {'Marge': 36}
    """
    return {k: v for k, v in d.items() if predicate(k)}


def filter_values(d: dict, predicate: Callable) -> dict:
    """
    Returns new subset dict of d where values pass predicate fn

    >>> d = {'Homer': 39, 'Marge': 36, 'Bart': 10}
    >>> filter_values(d, lambda x: x < 20)
    {'Bart': 10}
    """
    return {k: v for k, v in d.items() if predicate(v)}
