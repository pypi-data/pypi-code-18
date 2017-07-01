from typing import Any, Callable, Tuple, Iterable, TypeVar

from .curried import curried

T = TypeVar('T')


@curried
def tmap(func: Callable[[T], Any], iterable: Iterable[T]) -> Tuple:
    return tuple(map(func, iterable))


@curried
def tfilter(func: Callable[[T], bool], iterable: Iterable[T]) -> Tuple[T]:
    return tuple(filter(func, iterable))


def find(func: Callable[[T], bool], iterable: Iterable[T]) -> T:
    return next(filter(func, iterable))
