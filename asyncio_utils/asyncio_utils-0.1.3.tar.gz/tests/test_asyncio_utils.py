#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test_asyncio_utils
----------------------------------

Tests for ``asyncio_utils``  module.
"""

import pytest
import collections

from asyncio_utils import *


pytestmark = pytest.mark.asyncio


async def test_aiter():
    async def gen():
        yield 1

    async for v in aiter(gen):  # oops, forgot to call gen()
        assert v == 1

    async for v in aiter(arange(1, 5)):
        assert v in range(1, 5)

    async for v in aiter(range(1, 5)):
        assert v in range(1, 5)


async def test_arange():
    myrange = await arange(1, 5)
    assert isinstance(myrange, collections.AsyncIterator)
    mylist = [n async for n in myrange]
    assert mylist == [1, 2, 3, 4]


async def test_transform_factory_with_async__type():

    async def type_fn(iterable):
        return set(iterable)

    myset = await transform_factory(arange(1, 5), _type=type_fn)
    assert myset == {1, 2, 3, 4}


async def test_transform_factory_fails_if_type_not_callable():
    with pytest.raises(TypeError):
        await transform_factory(await arange(1, 5), _type=None)


async def test_alist():
    mylist = await alist(arange(1, 5))
    assert mylist == [1, 2, 3, 4]


async def test_atuple():
    mytuple = await atuple(await arange(1, 5))
    assert mytuple == (1, 2, 3, 4)


async def test_amap():
    formatter = '${}'.format
    expects = ['$1', '$2', '$3', '$4']

    mymap = await alist(
        amap(formatter, arange(1, 5))
    )
    assert mymap == expects

    async def aformatter(val):
        return f'${val}'

    mymap2 = await alist(
        amap(aformatter, await arange(1, 5))
    )
    assert mymap2 == expects


async def test_anext():

    myrange = await arange(1, 5)
    for n in range(1, 5):
        val = await anext(myrange)
        assert val == n

    with pytest.raises(StopAsyncIteration):
        await anext(myrange)

    with pytest.raises(TypeError):
        await anext(iter(range(1, 5)))


async def test_anext_with_default_arg():

    myrange = await arange(1)
    assert await anext(myrange) == 0
    assert await anext(myrange, 3) == 3


async def test_anext_with_default_kwarg():

    myrange = await arange(1)
    assert await anext(myrange) == 0
    assert await anext(myrange, default=3) == 3


async def test_aset():
    myset = await aset(arange(1, 5))
    assert myset == {1, 2, 3, 4}


async def test_adict():
    async def k_v_gen():
        async for n in await arange(1, 5):
            yield (n, n * 2)

    mydict = await adict(k_v_gen())
    assert mydict == {1: 2, 2: 4, 3: 6, 4: 8}


async def test_make_async():

    def always_one():
        return 1

    async_always_one = make_async(always_one)
    assert await async_always_one() == always_one()


    @make_async
    class AlwaysOneClass(object):

        def __init__(self):
            self.value = 1

        def __repr__(self):
            return f'{self.__class__.__name__}(value={self.value})'

    expects = 'AlwaysOneClass(value=1)'
    assert repr(await AlwaysOneClass()) == expects


async def test_afilter():

    myrange = await arange(1, 5)
    myfilter = afilter(lambda x: x == 2, myrange)
    assert await anext(myfilter) == 2
    assert await anext(myfilter, None) is None

    async def filter_func(val):
        return val == 2

    myfilter2 = afilter(filter_func, arange(1, 5))
    assert await anext(myfilter2) == 2

    with pytest.raises(StopAsyncIteration):
        await anext(myfilter2)
