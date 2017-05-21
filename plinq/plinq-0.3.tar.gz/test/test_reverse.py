from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestReverse(TestBase):
    def test_iteration(self):
        """
        Tests that using reverse will not raise a TypeError when iteration starts
        Tests also, that reverse takes effect
        """
        self._test_range(self._linq.reverse(), [5, 4, 3, 2, 1])
        self._linq = Linq([Person("Name1", 55, []), Person("Name2", 44, []), Person("Name3", 33, [])])
        expected_values = [Person("Name3", 33, []), Person("Name2", 44, []), Person("Name1", 55, [])]
        self._test_range(self._linq.reverse(), expected_values)
        # Check with empty iterables
        self._test_range(Linq([]).reverse(), [])
