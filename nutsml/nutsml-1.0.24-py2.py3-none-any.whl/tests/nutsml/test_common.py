"""
.. module:: test_common
   :synopsis: Unit tests for common module
"""
import pytest

import numpy as np
import random as rnd

from six.moves import zip, range
from nutsflow import Consume, Collect, Map
from nutsml import SplitRandom, CheckNaN, PartitionByCol


def test_CheckNaN():
    assert [1, 2] >> CheckNaN() >> Collect() == [1, 2]

    with pytest.raises(RuntimeError) as ex:
        [1, np.NaN, 3] >> CheckNaN() >> Consume()
    assert str(ex.value).startswith('NaN encountered')

    with pytest.raises(RuntimeError) as ex:
        [(1, np.NaN), (2, 4)] >> CheckNaN() >> Consume()
    assert str(ex.value).startswith('NaN encountered')


def test_PartitionByCol():
    samples = [(1, 1), (2, 0), (2, 4), (1, 3), (3, 0)]

    ones, twos = samples >> PartitionByCol(0, [1, 2])
    assert ones == [(1, 1), (1, 3)]
    assert twos == [(2, 0), (2, 4)]

    twos, ones = samples >> PartitionByCol(0, [2, 1])
    assert ones == [(1, 1), (1, 3)]
    assert twos == [(2, 0), (2, 4)]

    ones, fours = samples >> PartitionByCol(0, [1, 4])
    assert ones == [(1, 1), (1, 3)]
    assert fours == []

    ones, twos = [] >> PartitionByCol(0, [1, 2])
    assert ones == []
    assert twos == []


def test_SplitRandom_split():
    train, val = range(1000) >> SplitRandom(ratio=0.7)
    assert len(train) == 700
    assert len(val) == 300
    assert not set(train).intersection(val)


def test_SplitRandom_ratios():
    train, val, test = range(1000) >> SplitRandom(ratio=(0.6, 0.3, 0.1))
    assert len(train) == 600
    assert len(val) == 300
    assert len(test) == 100

    with pytest.raises(ValueError) as ex:
        range(1000) >> SplitRandom(ratio=(0.6, 0.7))
    assert str(ex.value).startswith('Ratios must sum up to one')


def test_SplitRandom_seed():
    split1 = range(10) >> SplitRandom(rand=rnd.Random(0))
    split2 = range(10) >> SplitRandom(rand=rnd.Random(0))
    split3 = range(10) >> SplitRandom(rand=rnd.Random(1))
    assert split1 == split2
    assert split1 != split3


def test_SplitRandom_constraint():
    same_letter = lambda t: t[0]
    data = zip('aabbccddee', range(10))
    train, val = data >> SplitRandom(rand=rnd.Random(0), ratio=0.6,
                                     constraint=same_letter) >> Map(sorted)
    assert train == [('a', 0), ('a', 1), ('b', 2), ('b', 3), ('c', 4), ('c', 5)]
    assert val == [('d', 6), ('d', 7), ('e', 8), ('e', 9)]
