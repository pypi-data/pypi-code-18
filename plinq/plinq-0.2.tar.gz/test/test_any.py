from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestAny(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling any() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter predicate must be a callable
            self._linq.any(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling any() with the right parameter will not raise a TypeError
        """
        self.assertTrue(self._linq.any(lambda item: True))
        people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(people)
        self.assertTrue(self._linq.any(lambda person: person.age == 33))
        self.assertTrue(self._linq.any(self._predicate))
        self.assertFalse(self._linq.any(lambda person: person.age == 30))
        self.assertTrue(self._linq.any())

    def test_empty_range(self):
        """
        Tests that using any with empty range will return false
        """
        self._linq = Linq([])
        self.assertFalse(self._linq.any(lambda item: True))
        self.assertFalse(self._linq.any(lambda item: False))
        self.assertFalse(self._linq.any())

    @staticmethod
    def _predicate(person: Person) -> int:
        return person.age > 30
