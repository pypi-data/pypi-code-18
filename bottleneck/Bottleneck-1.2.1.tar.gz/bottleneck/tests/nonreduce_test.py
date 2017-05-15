"Test replace()."

import warnings

import numpy as np
from numpy.testing import assert_equal, assert_array_equal, assert_raises
import bottleneck as bn
from .util import arrays, array_order


def test_nonreduce():
    "test nonreduce functions"
    for func in bn.get_functions('nonreduce'):
        yield unit_maker, func


def unit_maker(func):
    "Test that bn.xxx gives the same output as np.xxx."
    msg = '\nfunc %s | input %s (%s) | shape %s | old %f | new %f | order %s\n'
    msg += '\nInput array:\n%s\n'
    name = func.__name__
    func0 = eval('bn.slow.%s' % name)
    rs = np.random.RandomState([1, 2, 3])
    news = [1, 0, np.nan, -np.inf]
    for i, arr in enumerate(arrays(name)):
        for idx in range(2):
            if arr.size == 0:
                old = 0
            else:
                idx = rs.randint(max(arr.size, 1))
                old = arr.flat[idx]
            for new in news:
                if not issubclass(arr.dtype.type, np.inexact):
                    if not np.isfinite(old):
                        # Cannot safely cast to int
                        continue
                    if not np.isfinite(new):
                        # Cannot safely cast to int
                        continue
                actual = arr.copy()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    func(actual, old, new)
                desired = arr.copy()
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    func0(desired, old, new)
                tup = (name, 'a'+str(i), str(arr.dtype),
                       str(arr.shape), old, new, array_order(arr), arr)
                err_msg = msg % tup
                assert_array_equal(actual, desired, err_msg=err_msg)
                err_msg += '\n dtype mismatch %s %s'
                if hasattr(actual, 'dtype') or hasattr(desired, 'dtype'):
                    da = actual.dtype
                    dd = desired.dtype
                    assert_equal(da, dd, err_msg % (da, dd))


# ---------------------------------------------------------------------------
# Check that exceptions are raised

def test_replace_unsafe_cast():
    "Test replace for unsafe casts"
    dtypes = ['int32', 'int64']
    for dtype in dtypes:
        a = np.zeros(3, dtype=dtype)
        assert_raises(ValueError, bn.replace, a.copy(), 0.1, 0)
        assert_raises(ValueError, bn.replace, a.copy(), 0, 0.1)
        assert_raises(ValueError, bn.slow.replace, a.copy(), 0.1, 0)
        assert_raises(ValueError, bn.slow.replace, a.copy(), 0, 0.1)


def test_non_array():
    "Test that non-array input raises"
    a = [1, 2, 3]
    assert_raises(TypeError, bn.replace, a, 0, 1)
    a = (1, 2, 3)
    assert_raises(TypeError, bn.replace, a, 0, 1)


# ---------------------------------------------------------------------------
# Make sure bn.replace and bn.slow.replace can handle int arrays where
# user wants to replace nans

def test_replace_nan_int():
    "Test replace, int array, old=nan, new=0"
    a = np.arange(2*3*4).reshape(2, 3, 4)
    actual = a.copy()
    bn.replace(actual, np.nan, 0)
    desired = a.copy()
    msg = 'replace failed on int input looking for nans'
    assert_array_equal(actual, desired, err_msg=msg)
    actual = a.copy()
    bn.slow.replace(actual, np.nan, 0)
    msg = 'slow.replace failed on int input looking for nans'
    assert_array_equal(actual, desired, err_msg=msg)
