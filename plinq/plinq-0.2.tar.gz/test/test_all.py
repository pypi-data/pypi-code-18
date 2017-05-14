from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestAll(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling all() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter predicate must be a callable
            self._linq.all(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter predicate cannot be None - it is not optional
            self._linq.all(None)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling all() with the right parameter will not raise a TypeError
        """
        self.assertTrue(self._linq.all(lambda item: True))
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertTrue(self._linq.all(lambda person: person.age < 40))
        self.assertTrue(self._linq.all(self._predicate))
        self.assertFalse(self._linq.all(lambda person: person.age < 30))

    def test_empty_range(self):
        """
        Tests that using all with empty range will return true
        """
        self._linq = Linq([])
        self.assertTrue(self._linq.all(lambda item: True))
        self.assertTrue(self._linq.all(lambda item: False))

    @staticmethod
    def _predicate(person: Person) -> int:
        return person.age < 40
