from test.test_base import TestBase
from plinq.linq import Linq


class TestSkip(TestBase):
    def test_valid_parameters(self):
        """
        Tests that calling skip() with the right parameter will not raise any error
        """

        self._test_range(self._linq.skip(1), [2, 3, 4, 5])
        self._test_range(self._linq.skip(2), [3, 4, 5])
        self._test_range(self._linq.skip(3), [4, 5])
        self._test_range(self._linq.skip(4), [5])

    def test_empty_range(self):
        """
        Tests that using skip with empty range will return another empty range
        """
        self._linq = Linq([])
        self._test_range(self._linq.skip(1), [])
        self._test_range(self._linq.skip(2), [])
        self._test_range(self._linq.skip(3), [])
        self._test_range(self._linq.skip(4), [])

    def test_too_high_count(self):
        """
        Tests that using equal or higher count value than the number of the items in the range, returns an empty range
        """
        self._test_range(self._linq.skip(5), [])
        self._test_range(self._linq.skip(6), [])

    def test_zero_count(self):
        """
        Tests the using a zero count value, will return the same range
        """
        self._test_range(self._linq.skip(0), [1, 2, 3, 4, 5])
