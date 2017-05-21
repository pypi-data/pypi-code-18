from test.test_base import TestBase
import plinq


class TestFromRange(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling plinq.from_range() should raise a TypeError, if parameters are not integers
        """
        with self.assertRaises(TypeError):
            # Parameters must be integers
            plinq.from_range(1.0, 5.0)
        with self.assertRaises(TypeError):
            # Parameters must be integers
            plinq.from_range("1", "10")

    def test_valid_parameters(self):
        """
        Tests that calling plinq.from_range() with valid parameters will not raise a TypeError
        """
        # Different types of ranges
        self._linq = plinq.from_range(1, 10)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_range(5, 10)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_range(5, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._linq = plinq.from_range(0, 0)
        self.assertIsInstance(self._linq, plinq.Linq)

    def test_iteration(self):
        """
        Tests that using plinq.from_range with the right parameters, will not raise a TypeError when iteration starts
        """
        self._linq = plinq.from_range(1, 6)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [1, 2, 3, 4, 5])
        self._linq = plinq.from_range(5, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
        self._linq = plinq.from_range(0, 0)
        self.assertIsInstance(self._linq, plinq.Linq)
        self._test_range(self._linq, [])
