from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestAverage(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling average() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.average(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling average() with the right parameter will not raise a TypeError
        """
        # Calculate average
        self.assertEqual(self._linq.average(), 3)
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertEqual(self._linq.average(lambda person: person.age), 22)
        self.assertEqual(self._linq.average(self._selector), 22)

    def test_empty_range(self):
        """
        Tests that using average with empty range will raise a ValueError
        """
        self._linq = Linq([])
        with self.assertRaises(ValueError) as context:
            self._linq.average()
        self.assertEqual(str(context.exception), "Operator 'average' cannot work on empty range")

    @staticmethod
    def _selector(person: Person) -> int:
        return person.age
