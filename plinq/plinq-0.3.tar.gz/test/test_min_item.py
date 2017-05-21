from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestMinItem(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling min_item() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.min_item(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling min_item() with the right parameter will not raise a TypeError
        """
        # Calculate min
        self.assertEqual(self._linq.min_item(), 1)
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertEqual(self._linq.min_item(lambda person: person.age), Person("Name1", 11))
        self.assertEqual(self._linq.min_item(self._selector), Person("Name1", 11))

    def test_empty_range(self):
        """
        Tests that using min_item with empty range will raise a ValueError
        """
        self._linq = Linq([])
        with self.assertRaises(ValueError) as context:
            self._linq.min_item()
        self.assertEqual(str(context.exception), "Operator 'min_item' cannot work on empty range")

    @staticmethod
    def _selector(person: Person) -> int:
        return person.age
