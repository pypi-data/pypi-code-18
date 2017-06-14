#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_asyncio_utils
----------------------------------

Tests for `asyncio_utils` module.
"""

import pytest
import collections


import asyncio_utils

pytestmark = pytest.mark.asyncio


async def test_aiter():
    iterator = await asyncio_utils.aiter(range(1, 5))
    assert isinstance(iterator, collections.AsyncIterator)

    mylist = [n async for n in iterator]
    assert mylist == [1, 2, 3, 4]


async def test_aiter_with_an_awaitable():

    async def awaitable_iterator():
        return range(1, 5)

    # not awaited for yet.
    not_awaited = awaitable_iterator()
    iterator = await asyncio_utils.aiter(not_awaited)
    assert isinstance(iterator, collections.AsyncIterator)

    mylist = [n async for n in iterator]
    assert mylist == [1, 2, 3, 4]


async def test_aiter_with_an_AsyncIterator():
    aiter = asyncio_utils._aiter_gen(range(1, 5))
    iterator = await asyncio_utils.aiter(aiter)
    assert iterator == aiter


async def test_arange():
    arange = await asyncio_utils.arange(1, 5)
    assert isinstance(arange, collections.AsyncIterator)

    mylist = [n async for n in arange]
    assert mylist == [1, 2, 3, 4]


async def test_transform_factory_with_async__type():

    async def type_fn(iterable):
        return set(iterable)

    mytuple = await asyncio_utils.transform_factory(asyncio_utils.arange(1, 5),
                                                    _type=type_fn)
    assert mytuple == {1, 2, 3, 4}


async def test_transform_factory_fails_if_type_not_callable():
    with pytest.raises(TypeError):
        await asyncio_utils.transform_factory(await asyncio_utils.arange(1, 5),
                                              _type=None)


async def test_alist():
    mylist = await asyncio_utils.alist(asyncio_utils.arange(1, 5))
    assert mylist == [1, 2, 3, 4]


async def test_atuple():
    mytuple = await asyncio_utils.atuple(await asyncio_utils.arange(1, 5))
    assert mytuple == (1, 2, 3, 4)


async def test_amap():
    formatter = '${}'.format
    expects = ['$1', '$2', '$3', '$4']

    mymap = await asyncio_utils.alist(
        asyncio_utils.amap(formatter, asyncio_utils.arange(1, 5))
    )
    assert mymap == expects

    async def aformatter(val):
        return f'${val}'

    mymap2 = await asyncio_utils.alist(
        asyncio_utils.amap(aformatter, await asyncio_utils.arange(1, 5))
    )
    assert mymap2 == expects


async def test_anext():

    myrange = await asyncio_utils.arange(1, 5)
    for n in range(1, 5):
        val = await asyncio_utils.anext(myrange)
        assert val == n

    with pytest.raises(StopAsyncIteration):
        await asyncio_utils.anext(myrange)

    with pytest.raises(TypeError):
        await asyncio_utils.anext(iter(range(1, 5)))


async def test_anext_with_default_arg():

    myrange = await asyncio_utils.arange(1)
    assert await asyncio_utils.anext(myrange) == 0
    assert await asyncio_utils.anext(myrange, 3) == 3


async def test_anext_with_default_kwarg():

    myrange = await asyncio_utils.arange(1)
    assert await asyncio_utils.anext(myrange) == 0
    assert await asyncio_utils.anext(myrange, default=3) == 3


async def test_aset():
    myset = await asyncio_utils.aset(asyncio_utils.arange(1, 5))
    assert myset == {1, 2, 3, 4}


async def test_adict():
    async def k_v_gen():
        async for n in await asyncio_utils.arange(1, 5):
            yield (n, n * 2)

    mydict = await asyncio_utils.adict(k_v_gen())
    assert mydict == {1: 2, 2: 4, 3: 6, 4: 8}
