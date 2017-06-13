import unittest
from threading_tools import SynchronizedNumber

NUM_TRIALS = 2500


class TestSynchronizedBasicMath(unittest.TestCase):

    #
    # testing __neg__()
    #

    def test_sync_neg(self):
        sync_num1 = SynchronizedNumber(50.0)

        res_sync_num = -sync_num1
        assert res_sync_num == -50, 'The sum should be -50. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the original obj.'

    #
    # testing __add__() and __radd__()
    #

    def test_sync_add(self):
        sync_num1 = SynchronizedNumber(50.0)
        sync_num2 = SynchronizedNumber(50.0)

        res_sync_num = sync_num1 + sync_num2
        assert res_sync_num == 100, 'The sum should be 100. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the addend obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the addend obj.'

    def test_non_sync_add(self):
        sync_num1 = SynchronizedNumber(50.0)

        res_sync_num = sync_num1 + 50
        assert res_sync_num == 100, 'The sum should be 100. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the addend obj.'

    def test_reverse_non_sync_add(self):
        sync_num1 = SynchronizedNumber(50.0)

        res_sync_num = 50 + sync_num1
        assert res_sync_num == 100, 'The sum should be 100. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the addend obj.'

    #
    # testing __sub__() and __rsub__()
    #

    def test_sync_sub(self):
        sync_num1 = SynchronizedNumber(50.0)
        sync_num2 = SynchronizedNumber(50.0)

        res_sync_num = sync_num1 - sync_num2
        assert res_sync_num == 0, 'The sum should be 0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the minuend obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the subtrahend obj.'

    def test_non_sync_sub(self):
        sync_num1 = SynchronizedNumber(50.0)

        res_sync_num = sync_num1 - 50
        assert res_sync_num == 0, 'The sum should be 0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the minuend obj.'

    def test_reverse_non_sync_sub(self):
        sync_num1 = SynchronizedNumber(50.0)

        res_sync_num = 60 - sync_num1
        assert res_sync_num == 10, 'The sum should be 10. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the subtrahend obj.'

    #
    # testing __mul__() and __rmul__()
    #

    def test_sync_mul(self):
        sync_num1 = SynchronizedNumber(4.0)
        sync_num2 = SynchronizedNumber(2.0)

        res_sync_num = sync_num1 * sync_num2
        assert res_sync_num == 8.0, 'The sum should be 8.0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the multiplicand obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the multiplicand obj.'

    def test_non_sync_mul(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = sync_num1 * 2
        assert res_sync_num == 8.0, 'The sum should be 8.0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the multiplicand obj.'

    def test_reverse_non_sync_mul(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = 2 * sync_num1
        assert res_sync_num == 8.0, 'The sum should be 8.0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the multiplicand obj.'

    #
    # testing __div__() and __rdiv__()
    #

    def test_sync_div(self):
        sync_num1 = SynchronizedNumber(4.0)
        sync_num2 = SynchronizedNumber(2.0)

        res_sync_num = sync_num1 / sync_num2
        assert res_sync_num == 2.0, 'The sum should be 2.0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the dividend obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the divisor obj.'

    def test_non_sync_div(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = sync_num1 / 2
        assert res_sync_num == 2.0, 'The sum should be 2.0. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the dividend obj.'

    def test_reverse_non_sync_div(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = 2 / sync_num1
        assert res_sync_num == 0.5, 'The sum should be 0.5. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the divisor obj.'

    #
    # testing __pow__() and __rpow__()
    #

    def test_sync_pow(self):
        sync_num1 = SynchronizedNumber(4.0)
        sync_num2 = SynchronizedNumber(2.0)

        res_sync_num = sync_num1 ** sync_num2
        assert res_sync_num == 16, 'The sum should be 16. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the base obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the exponent obj.'

    def test_non_sync_pow(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = sync_num1 ** 2
        assert res_sync_num == 16, 'The sum should be 16. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the base obj.'

    def test_reverse_non_sync_pow(self):
        sync_num1 = SynchronizedNumber(4.0)

        res_sync_num = 2 ** sync_num1
        assert res_sync_num == 16, 'The sum should be 16. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the exponent obj.'

    #
    # testing __mod__() and __rmod__()
    #

    def test_sync_mod(self):
        sync_num1 = SynchronizedNumber(5.0)
        sync_num2 = SynchronizedNumber(2.0)

        res_sync_num = sync_num1 % sync_num2
        assert res_sync_num == 1, 'The sum should be 1. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the dividend obj.'
        assert res_sync_num is not sync_num2, 'The result obj should not be the divisor obj.'

    def test_non_sync_mod(self):
        sync_num1 = SynchronizedNumber(5.0)

        res_sync_num = sync_num1 % 2
        assert res_sync_num == 1, 'The sum should be 1. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the dividend obj.'

    def test_reverse_non_sync_mod(self):
        sync_num1 = SynchronizedNumber(2.0)

        res_sync_num = 5 % sync_num1
        assert res_sync_num == 1, 'The sum should be 1. Instead it is {0}'.format(res_sync_num)
        assert res_sync_num is not sync_num1, 'The result obj should not be the divisor obj.'
