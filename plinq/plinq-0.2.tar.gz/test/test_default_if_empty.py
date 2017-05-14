from test.test_base import TestBase
from test.utils import Person
import plinq


class TestDefaultIfEmpty(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling plinq.default_if_empty() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            plinq.default_if_empty(5, None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling plinq.default_if_empty() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq = plinq.default_if_empty([], None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.default_if_empty({}, None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.default_if_empty(set(), None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.default_if_empty("", None)
        self.assertIsInstance(self._linq, plinq.Linq)

    def test_iteration(self):
        """
        Tests that using plinq.default_if_empty with the right parameter, will not raise a TypeError when iteration starts
        """
        self._linq = plinq.default_if_empty([1, 2, 3, 4, 5], None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [1, 2, 3, 4, 5])
        self._linq = plinq.default_if_empty([], -1)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [-1])
        self._linq = plinq.default_if_empty(dict(a=1, b=2, c=3), None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_set(self._linq, {"a", "b", "c"})
        self._linq = plinq.default_if_empty({}, -1)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [-1])
        self._linq = plinq.default_if_empty(set(), -1)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [-1])
        self._linq = plinq.default_if_empty([Person("Name1", 11), Person("Name2", 22)], None)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [Person("Name1", 11), Person("Name2", 22)])
