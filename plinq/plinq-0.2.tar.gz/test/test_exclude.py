from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq
from test.utils import FakeIteratorIterable


class TestExclude(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling exclude() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.exclude(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.exclude(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.exclude(FakeIteratorIterable())
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling exclude() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq.exclude([])
        self._linq.exclude({})
        self._linq.exclude(set())
        self._linq.exclude("")

    def test_iteration(self):
        """
        Tests that using exclude with the right parameter, will not raise a TypeError when iteration starts
        Tests also, that exclude takes effect
        """
        self._test_set(self._linq.exclude([1, 2, 3, 4, 5]), set())
        self._test_set(self._linq.exclude([]), {1, 2, 3, 4, 5})
        self._test_set(self._linq.exclude([1, 2]), {3, 4, 5})
        self._linq = Linq([Person("Name1", 11, []), Person("Name2", 22, []), Person("Name3", 33, [])])
        self._test_set(self._linq.exclude([Person("Name1", 11, [])]),
                       {Person("Name2", 22, []), Person("Name3", 33, [])})
