from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestToList(TestBase):
    def test_invocation(self):
        """
        Tests that using to_list will not raise a TypeError when called 
        Tests also, that to_list takes effect
        """
        self.assertEqual(self._linq.to_list(), [1, 2, 3, 4, 5])
        self._linq = Linq([Person("Name1", 55, []), Person("Name2", 44, []), Person("Name3", 33, [])])
        expected_values = [Person("Name1", 55, []), Person("Name2", 44, []), Person("Name3", 33, [])]
        self.assertEqual(self._linq.to_list(), expected_values)
        # Check with empty iterables
        self._linq = Linq([])
        self.assertEqual(self._linq.to_list(), [])
