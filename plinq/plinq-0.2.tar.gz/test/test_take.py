from test.test_base import TestBase
from plinq.linq import Linq


class TestTake(TestBase):
    def test_valid_parameters(self):
        """
        Tests that calling take() with the right parameter will not raise any error
        """

        self._test_range(self._linq.take(1), [1])
        self._test_range(self._linq.take(2), [1, 2])
        self._test_range(self._linq.take(3), [1, 2, 3])
        self._test_range(self._linq.take(4), [1, 2, 3, 4])

    def test_empty_range(self):
        """
        Tests that using take with empty range will return another empty range
        """
        self._linq = Linq([])
        self._test_range(self._linq.take(1), [])
        self._test_range(self._linq.take(2), [])
        self._test_range(self._linq.take(3), [])
        self._test_range(self._linq.take(4), [])

    def test_too_high_count(self):
        """
        Tests that using equal or higher count value than the number of the items in the range, returns the whole range
        """
        self._test_range(self._linq.take(5), [1, 2, 3, 4, 5])
        self._test_range(self._linq.take(6), [1, 2, 3, 4, 5])

    def test_zero_count(self):
        """
        Tests the using a zero count value, will an empty range
        """
        self._test_range(self._linq.take(0), [])
