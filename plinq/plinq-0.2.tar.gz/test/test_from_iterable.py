from test.test_base import TestBase
from test.utils import Person
import plinq


class TestFromIterable(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling plinq.from_iterable() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            plinq.from_iterable(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            plinq.from_iterable(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling plinq.from_iterable() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq = plinq.from_iterable([])
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_iterable({})
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_iterable(set())
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_iterable("")
        self.assertIsInstance(self._linq, plinq.Linq)

    def test_iteration(self):
        """
        Tests that using plinq.from_iterable with the right parameter, will not raise a TypeError when iteration starts
        """
        self._linq = plinq.from_iterable([1, 2, 3, 4, 5])
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [1, 2, 3, 4, 5])
        self._linq = plinq.from_iterable([])
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
        self._linq = plinq.from_iterable(dict(a=1, b=2, c=3))
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_set(self._linq, {"a", "b", "c"})
        self._linq = plinq.from_iterable([Person("Name1", 11), Person("Name2", 22)])
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [Person("Name1", 11), Person("Name2", 22)])
