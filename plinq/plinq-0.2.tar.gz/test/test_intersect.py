from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq
from test.utils import FakeIteratorIterable


class TestIntersect(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling intersect() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.intersect(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.intersect(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.intersect(FakeIteratorIterable())
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling intersect() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq.intersect([])
        self._linq.intersect({})
        self._linq.intersect(set())
        self._linq.intersect("")

    def test_iteration(self):
        """
        Tests that using intersect with the right parameter, will not raise a TypeError when iteration starts
        Tests also, that intersect takes effect
        """
        self._test_set(self._linq.intersect([1, 2, 3, 4, 5]), {1, 2, 3, 4, 5})
        self._test_set(self._linq.intersect([]), set())
        self._test_set(self._linq.intersect([1, 2]), {1, 2})
        self._linq = Linq([Person("Name1", 11, []), Person("Name2", 22, []), Person("Name3", 33, [])])
        self._test_set(self._linq.intersect([Person("Name1", 11, [])]), {Person("Name1", 11, [])})
