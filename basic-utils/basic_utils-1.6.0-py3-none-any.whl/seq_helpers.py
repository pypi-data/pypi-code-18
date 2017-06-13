from functools import reduce
from itertools import chain, groupby, islice
from operator import itemgetter
from typing import Any, Callable, Iterable, Sequence

__all__ = [
    'all_equal',
    'butlast',
    'concat',
    'cons',
    'dedupe',
    'first',
    'flatten',
    'head',
    'init',
    'last',
    'nth',
    'partial_flatten',
    'quantify',
    'rest',
    'reverse',
    'sorted_index',
    'tail',
    'take',
]


def first(seq: Sequence) -> Any:
    """
    Returns first element in a sequence.

    >>> first([1, 2, 3])
    1
    """
    return next(iter(seq))


def second(seq: Sequence) -> Any:
    """
    Returns second element in a sequence.

    >>> second([1, 2, 3])
    2
    """
    return seq[1]


def last(seq: Sequence) -> Any:
    """
    Returns the last item in a Sequence

    >>> last([1, 2, 3])
    3
    """
    return seq[-1]


def butlast(seq: Sequence) -> Sequence:
    """
    Returns all but the last item in sequence

    >>> butlast([1, 2, 3])
    [1, 2]
    """
    return seq[:-1]


def rest(seq: Sequence) -> Any:
    """
    Returns remaining elements in a sequence

    >>> rest([1, 2, 3])
    [2, 3]
    """
    return seq[1:]


def reverse(seq: Sequence) -> Sequence:
    """
    Returns sequence in reverse order

    >>> reverse([1, 2, 3])
    [3, 2, 1]
    """
    return seq[::-1]


def cons(item: Any, seq: Sequence) -> chain:
    """ Adds item to beginning of sequence.

    >>> list(cons(1, [2, 3]))
    [1, 2, 3]
    """
    return chain([item], seq)


def lazy_flatten(seq: Iterable) -> Iterable:
    """
    Returns a generator which yields items from a flattened version
    of the sequence.
    """
    for item in seq:
        if isinstance(item, Iterable) and not isinstance(item, (str, bytes)):
            yield from flatten(item)
        else:
            yield item


def flatten(seq: Iterable) -> Iterable:
    """ Returns a flatten version of sequence.

    >>> flatten([1, [2, [3, [4, 5], 6], 7]])
    [1, 2, 3, 4, 5, 6, 7]
    """
    return type(seq)(lazy_flatten(seq))  # type: ignore


def partial_flatten(seq: Iterable) -> Iterable:
    """
    Returns partially flattened version of sequence.

    >>> partial_flatten(((1,), [2, 3], (4, [5, 6])))
    (1, 2, 3, 4, [5, 6])
    """
    return type(seq)(reduce(concat, seq))  # type: ignore


def lazy_dedupe(seq: Sequence, key: Callable=None) -> Iterable:
    """
    Returns a generator which which yields items in the sequence skipping
    duplicates.
    """
    seen = set()  # type: set
    for item in seq:
        val = item if key is None else key(item)
        if val not in seen:
            yield item
            seen.add(val)


def sorted_index(seq: Sequence, item: Any, key: str=None) -> int:
    """
    >>> sorted_index([10, 20, 30, 40, 50], 35)
    3
    """
    keyfn = itemgetter(key) if key is not None else None
    cp = sorted(cons(item, seq), key=keyfn)
    return cp.index(item)


def dedupe(seq: Sequence, key: Callable=None) -> Iterable:
    """
    Removes duplicates from a sequence while maintaining order

    >>> dedupe([1, 5, 2, 1, 9, 1, 5, 10])
    [1, 5, 2, 9, 10]
    """
    return type(seq)(lazy_dedupe(seq, key))  # type: ignore


def concat(seqX: Sequence, seqY: Sequence) -> Sequence:
    """
    Joins two sequences together, returning a single combined sequence.
    Preserves the type of passed arguments.

    >>> concat((1, 2, 3), (4, 5, 6))
    (1, 2, 3, 4, 5, 6)
    """
    chained = chain(seqX, seqY)
    if type(seqX) == type(seqY):
        return type(seqX)(chained)  # type: ignore
    return list(chained)


def take(n: int, iterable: Iterable) -> Iterable:
    """
    Return first n items of the iterable as a list.

    >>> take(2, range(1, 10))
    [1, 2]
    """
    return list(islice(iterable, n))


def nth(iterable: Iterable, n: int, default: Any=None) -> Any:
    """
    Returns the nth item or a default value.

    >>> nth([1, 2, 3], 1)
    2
    """
    return next(islice(iterable, n, None), default)


def all_equal(iterable: Iterable) -> bool:
    """
    Returns True if all the elements are equal to each other.

    >>> all_equal([True, True])
    True
    """
    g = groupby(iterable)
    return next(g, True) and not next(g, False)  # type: ignore


def quantify(iterable: Iterable, pred: Callable=bool) -> int:
    """
    Returns count of how many times the predicate is true.

    >>> quantify([True, False, True])
    2
    """
    return sum(map(pred, iterable))


# Define some common aliases
head = first
tail = rest
init = butlast
