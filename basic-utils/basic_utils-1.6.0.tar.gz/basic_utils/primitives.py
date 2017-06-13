from functools import reduce
from operator import not_
from typing import Any, Callable, Iterator

__all__ = [
    'comp',
    'complement',
    'compose',
    'dec',
    'even',
    'identity',
    'inc',
    'natural_nums',
    'odd',
]

sentinel = object()


def natural_nums(start: int=0, end: int=None) -> Iterator[int]:
    """
    Yields a lazy sequence of natural numbers

    >>> from itertools import islice
    >>> list(islice(natural_nums(5), 3))
    [5, 6, 7]
    """

    while True:
        yield start
        start += 1
        if start == end:
            break


def identity(x: Any) -> Any:
    """
    Returns the same values passed as arguments

    >>> x = (10, 20)
    >>> identity(x)
    (10, 20)
    """
    return x


def comp(*funcs: Callable) -> Callable:
    """
    Takes a set of functions and returns a fn that is the composition
    of those functions
    """
    return reduce(lambda f, g: lambda x: f(g(x)), funcs, lambda x: x)


def complement(fn: Callable) -> Callable:
    """
    Takes a function fn and returns a function that takes the same arguments
    as fn with the opposite truth value.

    >>> not_five = complement(lambda x: x == 5)
    >>> not_five(6)
    True
    """
    return comp(not_, fn)


def inc(n: int) -> int:
    """
    Increments n by 1

    >>> inc(10)
    11
    """
    return n + 1


def dec(n: int) -> int:
    """
    Decrements n by 1

    >>> dec(5)
    4
    """
    return n - 1


def even(n: int) -> bool:
    """
    Returns true if n is even

    >>> even(2)
    True
    """
    return n % 2 == 0


def odd(n: int) -> bool:
    """
    Returns true if n is odd

    >>> even(3)
    False
    """
    return n % 2 == 1


# Define some common aliases
compose = comp
