from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestMaxItem(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling max_item() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.max_item(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling max_item() with the right parameter will not raise a TypeError
        """
        # Calculate max
        self.assertEqual(self._linq.max_item(), 5)
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertEqual(self._linq.max_item(lambda person: person.age), Person("Name3", 33))
        self.assertEqual(self._linq.max_item(self._selector), Person("Name3", 33))

    def test_empty_range(self):
        """
        Tests that using max_item with empty range will raise a ValueError
        """
        self._linq = Linq([])
        with self.assertRaises(ValueError) as context:
            self._linq.max_item()
        self.assertEqual(str(context.exception), "Operator 'max_item' cannot work on empty range")

    @staticmethod
    def _selector(person: Person) -> int:
        return person.age
