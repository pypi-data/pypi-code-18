# -*- coding: utf-8 -*-

import typing
import collections
import inspect
import functools


__author__ = """Michael Housh"""
__email__ = 'mhoush@houshhomeenergy.com'
__version__ = '0.1.3'

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
    'afilter',

    # non-async
    'make_async',
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


async def aiter(val):
    """An ``async generator`` that creates/ensures an ``AsyncIterator``.  This
    method will always try to do the right thing and return an
    ``AsyncIterator``.

    If the input is ``Awaitable``, then we will ``await`` the result, and check
    if it returns and ``AsyncIterator``.

    If the input is an ``async generator`` that was not called, then we will
    call it and yield it's values.

    Else if the input is an ``iterator`` we iterate it and yield the values.

    Example::

        >>> async def main():
                async for v in aiter2(range(1, 5)):  # normal iterator
                    print(v)

        >>> loop.run_until_complete(main())
        1
        2
        3
        4

        >>> async def main():
                async for v in aiter2(arange(1, 5)):  # not awaited
                    print(v)

        >>> loop.run_until_complete(main())
        1
        2
        3
        4

        >>> async def main():
                async for v in aiter2(await arange(1, 5)):  # awaited works
                    print(v)

        >>> loop.run_until_complete(main())
        1
        2
        3
        4

        >>> async def agen():
                yield 1
                yield 2
                yield 3
                yield 4

        >>> async def main():
                async for v in aiter2(agen):  # oops forgot to call it
                    print(v)

        >>> loop.run_until_complete(main())
        1
        2
        3
        4

    """
    if inspect.isawaitable(val):
        val = await val

    if inspect.isasyncgenfunction(val):
        val = val()

    if isinstance(val, collections.AsyncIterator):
        async for v in val:
            yield v
    else:
        for v in iter(val):
            yield v


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

    iterator = aiter(iterator)

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
    return aiter(range(*args, **kwargs))


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
    async for val in aiter(iterator):
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


async def afilter(filter_func: typing.Callable[[typing.Any], bool],
                  iterator: IteratorType) -> typing.Iterator[typing.Any]:

    async for val in aiter(iterator):
        if inspect.iscoroutinefunction(filter_func):
            check = await filter_func(val)
        else:
            check = filter_func(val)

        if check is True:
            yield val


def make_async(fn):
    """Makes a normal function (or class) ``Awaitable``.  This can be useful if
    you need an async and non-async version of the same method/class.

    Can be used as a decorator or called with a single input.

    :param fn:  The method/class to wrap and make async.

    Example::

        >>> @make_async
            def my_non_async_func():
                return 1

        >>> async def main():
                print(await my_non_async_func() == 1)

        >>> loop.run_until_complete(main())
        True

    Non Decorator Example::

        >>> class AlwaysOneClass(object):
                def __init__(self):
                    self.value = 1
                def __repr__(self):
                    return f'{self.__class__.__name__}(value={self.value})'

        >>> async_one_class_factory = make_async(AlwaysOneClass)

        >>> async def main():
                print(repr(await async_one_class_factory()))

        >>> loop.run_until_complete(main())
        AlwaysOneClass(value=1)

    """
    @functools.wraps(fn)
    async def decorator(*args, **kwargs):
        return fn(*args, **kwargs)

    return decorator
