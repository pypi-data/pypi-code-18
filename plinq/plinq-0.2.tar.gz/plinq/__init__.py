import typing
from plinq.linq import Linq

__all__ = []


def from_iterable(iterable: typing.Iterable) -> Linq:
    """
    Helper method to create a Linq from any iterable
    :param iterable: The iterable as the source of Linq
    :return: A new Linq object, wrapping the provided iterable
    """
    return Linq(iterable)


def default_if_empty(iterable: typing.Iterable, default: typing.Any) -> Linq:
    """
    Implements the default if empty linq operator
    :param iterable: The iterable to use as a source if it is not empty
    :param default: The default value to use as the only item in Linq if iterable is empty
    :return: A new Linq object, wrapping the iterable it it is not empty
             or wrapping a list with only one item, which is the default
    """
    if not iterable:
        iterable = [default]
    return Linq(iterable)


def empty() -> Linq:
    """
    Implements the empty linq operator
    :return: A new empty Linq object
    """
    return Linq([])


# TODO: Figure out how to have the same signature as the built-in range
def from_range(start: int, stop: int) -> Linq:
    """
    Implements the range linq operator.
    The name has to be changes, since range is a built-in name in Python
    :param start: The integer to start the range from
    :param stop: The integer to stop the range at
    :return: A new Linq object holding items from start to stop
    """
    r = range(start, stop)
    return Linq(list(r))


def repeat(value: typing.Any, count: int) -> Linq:
    """
    Implements the repeat linq operator
    :param value: The value to be inserted into the range object
    :param count: The number of wanted items in the range
    :return: A new Linq object holding 'count' number of items with the value of 'value'
    """
    r = []
    for i in range(count):
        r.append(value)
    return Linq(r)
