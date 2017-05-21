from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq
from test.utils import FakeIteratorIterable


class TestUnion(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling union() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.union(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.union(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.union(FakeIteratorIterable())
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling union() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq.union([])
        self._linq.union({})
        self._linq.union(set())
        self._linq.union("")

    def test_iteration(self):
        """
        Tests that using union with the right parameter, will not raise a TypeError when iteration starts
        Tests also, that union takes effect
        """
        self._test_set(self._linq.union([1, 2, 3, 4, 5]), {1, 2, 3, 4, 5})
        self._test_set(self._linq.union([]), {1, 2, 3, 4, 5})
        self._test_set(self._linq.union([1, 2]), {1, 2, 3, 4, 5})
        self._test_set(self._linq.union([6, 7]), {1, 2, 3, 4, 5, 6, 7})
        self._linq = Linq([Person("Name1", 11, [])])
        self._test_set(self._linq.union([Person("Name2", 22, [])]), {Person("Name1", 11, []), Person("Name2", 22, [])})
