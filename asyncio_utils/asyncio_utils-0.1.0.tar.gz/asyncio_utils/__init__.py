# -*- coding: utf-8 -*-

import typing
import collections
import inspect
import functools


__author__ = """Michael Housh"""
__email__ = 'mhoush@houshhomeenergy.com'
__version__ = '0.1.0'

__all__ = (
    'aiter',
    'arange',
    'transform_factory',
    'alist',
    'atuple',
    'aset',
    'adict',
    'amap',
    'anext',

    # non-async
    'make_aiter',
)



IteratorType = typing.Union[
    typing.Iterator[typing.Any],
    typing.AsyncIterator[typing.Any],
    typing.Iterable[typing.Any],
    typing.AsyncIterable[typing.Any]
]


TransformType = typing.Callable[
    [typing.Iterable[typing.Any]],  # *args(input) type
    typing.Any  # return type
]


async def _aiter_gen(iterator):
    """Turns a regular iterator into an async iterator."""
    for val in iter(iterator):
        yield val


def make_aiter(iterator) -> typing.Union[typing.Awaitable, typing.AsyncIterator]:
    """Non-async method that Wraps an iterator in an
    :class:`collections.AsyncIterator`.  If the input has not been awaited on
    (is a coroutine) or is already and AsyncIterator, then we do nothing and
    return the input.

    :param iterator:  The input value to wrap/ensure is an AsyncIterator.

    """
    if isinstance(iterator, collections.Awaitable) or \
            inspect.isawaitable(iterator) or \
            isinstance(iterator, collections.AsyncIterator):
        return iterator
    return _aiter_gen(iterator)


async def aiter(iterator) -> typing.AsyncIterator[typing.Any]:
    """Coroutine that wraps/ensures an ``AsyncIterator``.
    If the input has not been awaited on then we will await for the result.
    If the input (or awaited result) is already an
    ``AsyncIterator``, then we will return the input.  If it is
    not an ``AsyncIterator`` but is an iterable then we will wrap it and
    make an ``AsyncIterator``.

    :param iterator:  The iterator to wrap/ensure is an
                      :class:`collections.AsyncIterator`.


    Example::

        >>> async def main():
                # wraps a normal type that is iterable.
                iterator = await aiter(range(1, 5))
                async for n in iterator:
                    print(n)

        >>> loop.run_until_complete(main())
        1
        2
        3
        4

        >>> async def main():
                # returns the same input if the input is already an
                # AsyncIterator
                aiterator = await arange(1, 5)
                make_aiter = await aiter(aiterator)
                print(make_aiter == aiterator)

        >>> loop.run_until_complete(main())
        True

        >>> async def main():
                # will await on an object if needed, to see if it returns
                # an AsyncIterator
                async for n in aiter(arange(1)):  # arange not awaited
                    print(n)

        >>> loop.run_until_complete(main())
        0

    """
    if inspect.isawaitable(iterator) or \
            isinstance(iterator, collections.Awaitable):
        iterator = await iterator
    return make_aiter(iterator)


async def transform_factory(iterator: IteratorType, _type: TransformType=None
                            ) -> typing.Any:
    """Transform an ``AsyncIterator`` (really any iterator) to the
    ``_type``.  This is the base for the :func:`alist` and :func:`atuple`.

    :param iterator:  The :class:`AsyncIterator` to transform
    :param _type:  A callable (or coroutine) that is called with the result of
                   the ``iterator``.

    :raises TypeError:  If the ``_type`` is not callable.


    Example::

        >>> aset = functools.partial(transform_factory, _type=set)

        >>> async def main():
                print(await aset(arange(1, 5)))

        >>> loop.run_until_complete(main())
        {1, 2, 3, 4}

        # can also use a coroutine function as the _type callable.
        >>> async def async_type_func(iterable):
                return set(iterable)

        >>> aset2 = functools.partial(transform_factory, _type=async_set_func)

        >>> async def main():
                print(await aset2(await arange(1, 5)))

        >>> loop.run_until_complete(main())


    """
    if not callable(_type):
        raise TypeError('{} is not callable'.format(_type))

    iterator = await aiter(iterator)

    if inspect.iscoroutinefunction(_type):
        return await _type(iter([v async for v in iterator]))
    return _type(iter([v async for v in iterator]))


async def arange(*args, **kwargs
                 ) -> typing.AsyncIterator[typing.Union[int, float]]:
    """Mimics the builtin ``range``.  Returning an AsyncIterator for the passed
    in args, kwargs.

    :param args:  Passed to the builtin ``range`` method.
    :param kwargs:  Passed to the builtin ``range`` method.

    """
    return await aiter(range(*args, **kwargs))


alist = functools.partial(transform_factory, _type=list)
alist.__doc__ = """
Transform an ``AsyncIterator`` to a list.  This would be equivalent to
```[v async for v in async_iterator]```.

:param iterator:  The ``AsyncIterator`` to transform to a list.


Example::

    >>> async def main():
            print(await alist(arange(1, 5)))

    >>> loop.run_until_complete(main())
    [1, 2, 3, 4]

:rtype: list

"""


atuple = functools.partial(transform_factory, _type=tuple)
atuple.__doc__ = """
Transform an :class:`AsyncIterator` to a list.  This would be equivalent to
```tuple([v async for v in async_iterator])```.

:param iterator:  The ``AsyncIterator`` to transform to a tuple.


Example::

    >>> async def main():
            print(await atuple(arange(1, 5)))

    >>> loop.run_until_complete(main())
    (1, 2, 3, 4)

:rtype: tuple

"""

aset = functools.partial(transform_factory, _type=set)
aset.__doc__ = """
Transform an ``AsyncIterator`` into a set.  This would be equivalent to.
```{v async for v in async_iterator}```

However we ensure that the ``async_iterator`` is an ``AsyncIterator``.

Example::

    >>> async def main():
            print(await aset(arange(1, 5)))

    >>> loop.run_until_complete(main())
    {1, 2, 3, 4}

"""


adict = functools.partial(transform_factory, _type=dict)
adict.__doc__ = """
Transform an ``AsyncIterator`` into a dict.  This would be equivalent to.
```{k: v async for (k, v) in async_iterator}```

However we ensure that the ``async_iterator`` is an ``AsyncIterator``.

Example::

    >>> async def k_v_gen():
            for n in await arange(1, 5):
                yield n, n * 2

    >>> async def main():
            print(await adict(k_v_gen()))

    >>> loop.run_until_complete(main())
    {1: 2, 2: 4, 3: 6, 4: 8}

"""


async def amap(afunc: typing.Callable[[typing.Any], typing.Any],
               iterator: IteratorType) -> typing.AsyncIterator[typing.Any]:
    """An ``AsyncGenerator`` that mimics the builtin ``map`` method.

    :param afunc:  A callable (or coroutine) to call on each item of the
                   iterator.
    :param iterator:  An ``AsyncIterator`` to call the ``afunc`` on each of the
                      values.  If this is not an ``AsyncIterator`` we will turn
                      it into one and use ``async for`` to loop over the values.


    Example::

        >>> async def main():
                mymap = amap('${}'.format, arange(1, 5))
                async for val in mymap:
                    print(val)

        >>> loop.run_until_complete(main())
        $1
        $2
        $3
        $4

        # use a coroutine function as the func.
        >>> async def async_formatter(val):
                return f'{val}'

        >>> async def main():
                print(await alist(amap(async_formatter, arange(1, 5))))

        >>> loop.run_until_complete(main())
        ['$1', '$2', '$3', '$4']


    """
    async for val in await aiter(iterator):
        if inspect.iscoroutinefunction(afunc):
            yield await afunc(val)
        else:
            yield afunc(val)


async def anext(iterator: typing.AsyncIterator[typing.Any], *args, **kwargs
                ) -> typing.Any:
    """Mimics the builtin ``next`` for an ``AsyncIterator``.

    :param iterator:  An ``AsyncIterator`` to get the next value from.
    :param default:  Can be supplied as second arg or as a kwarg.  If a value is
                     supplied in either of those positions then a
                     ``StopAsyncIteration`` will not be raised and the
                     ``default`` will be returned.

    :raises TypeError:  If the input is not a :class:`collections.AsyncIterator`


    Example::

        >>> async def main():
                myrange = await arange(1, 5)
                for n in range(1, 5):
                    print(n, n == await anext(myrange))
                try:
                    n = await anext(myrange)
                    print("This should not be shown")
                except StopAsyncIteration:
                    print('Sorry no more values!')

        >>> loop.run_until_complete(main())
        1 True
        2 True
        3 True
        4 True
        Sorry no more values!


    """
    if not isinstance(iterator, collections.AsyncIterator):
        raise TypeError(f'Not an AsyncIterator: {iterator}')

    use_default = False
    default = None

    if len(args) > 0:
        default = args[0]
        use_default = True
    else:
        if 'default' in kwargs:
            default = kwargs['default']
            use_default = True

    try:
        return await iterator.__anext__()
    except StopAsyncIteration:
        if use_default:
            return default
        raise StopAsyncIteration
