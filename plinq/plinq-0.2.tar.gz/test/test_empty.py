from test.test_base import TestBase
import plinq


class TestReverse(TestBase):
    def test_iteration(self):
        """
        Tests that using plinq.empty() will not raise a TypeError when iteration starts
        """
        self._linq = plinq.empty()
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
