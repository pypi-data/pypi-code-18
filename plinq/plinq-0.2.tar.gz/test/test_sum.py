from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestSum(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling sum() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.sum(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling sum() with the right parameter will not raise a TypeError
        """
        # Calculate sum
        self.assertEqual(self._linq.sum(), 15)
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertEqual(self._linq.sum(lambda person: person.age), 66)
        self.assertEqual(self._linq.sum(self._selector), 66)

    def test_empty_range(self):
        """
        Tests that using sum with empty range will return zero
        """
        self._linq = Linq([])
        self.assertEqual(self._linq.sum(), 0)

    @staticmethod
    def _selector(person: Person) -> int:
        return person.age
