from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestContains(TestBase):
    def test_valid_parameters(self):
        """
        Tests that calling contains() with the right parameter will not raise any error
        """
        self.assertTrue(self._linq.contains(1))
        self.assertTrue(self._linq.contains(2))
        self.assertFalse(self._linq.contains(6))
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertTrue(self._linq.contains(Person("Name1", 11)))
        self.assertTrue(self._linq.contains(Person("Name2", 22)))
        self.assertFalse(self._linq.contains(Person("Name6", 66)))

    def test_empty_range(self):
        """
        Tests that using contains with empty range will return false
        """
        self._linq = Linq([])
        self.assertFalse(self._linq.contains(1))
        self.assertFalse(self._linq.contains(1.0))
        self.assertFalse(self._linq.contains("1"))
