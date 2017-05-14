from test.test_base import TestBase
from test.utils import Person
import plinq


class TestRepeat(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling plinq.repeat() should raise a TypeError, if count parameter is not an integer
        """
        with self.assertRaises(TypeError):
            # Parameter iterable must be an iterable
            plinq.repeat(None, 5.0)
        with self.assertRaises(TypeError):
            # Parameter iterable cannot be None - it is not optional
            plinq.repeat(None, "10")

    def test_valid_parameters(self):
        """
        Tests that calling plinq.repeat() with valid parameters will not raise a TypeError
        """
        # Different types of iterables
        self._linq = plinq.repeat(1, 10)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.repeat(5, 10)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.repeat(5, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.repeat(0, 0)
        self.assertIsInstance(self._linq, plinq.Linq)

    def test_iteration(self):
        """
        Tests that using plinq.repeat with the right parameters, will not raise a TypeError when iteration starts
        """
        self._linq = plinq.repeat(1, 6)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [1, 1, 1, 1, 1, 1])
        self._linq = plinq.repeat(5, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
        self._linq = plinq.repeat(0, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
        self._linq = plinq.repeat("1", 6)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, ["1", "1", "1", "1", "1", "1"])
        self._linq = plinq.repeat(1.1, 6)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [1.1, 1.1, 1.1, 1.1, 1.1, 1.1])
        self._linq = plinq.repeat(Person("Name1", 11), 2)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [Person("Name1", 11), Person("Name1", 11)])
        self._linq = plinq.repeat([], 2)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [[], []])
