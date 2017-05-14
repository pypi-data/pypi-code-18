from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestMin(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling min() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.min(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling min() with the right parameter will not raise a TypeError
        """
        # Calculate min
        self.assertEqual(self._linq.min(), 1)
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertEqual(self._linq.min(lambda person: person.age), 11)
        self.assertEqual(self._linq.min(self._selector), 11)

    def test_empty_range(self):
        """
        Tests that using min with empty range will raise a ValueError
        """
        self._linq = Linq([])
        with self.assertRaises(ValueError) as context:
            self._linq.min()
        self.assertEqual(str(context.exception), "Operator 'min' cannot work on empty range")

    @staticmethod
    def _selector(person: Person) -> int:
        return person.age
