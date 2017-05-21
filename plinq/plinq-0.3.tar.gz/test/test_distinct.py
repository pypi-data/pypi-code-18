from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestDistinct(TestBase):
    def setUp(self):
        self._linq = Linq([1, 1, 2, 3, 4, 4, 5, 5])

    def test_iteration(self):
        """
        Tests that using distinct will not raise a TypeError when iteration starts
        Tests also, that distinct takes effect
        """
        self._test_set(self._linq.distinct(), {1, 2, 3, 4, 5})
        self._linq = Linq([Person("Name1", 55, []), Person("Name1", 55, []), Person("Name3", 33, [])])
        expected_values = {Person("Name3", 33, []), Person("Name1", 55, [])}
        self._test_set(self._linq.distinct(), expected_values)
        # Check with empty iterables
        self._test_set(Linq([]).distinct(), set())
