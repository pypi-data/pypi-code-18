from test.test_base import TestBase
from plinq.linq import Linq


class TestSequenceEqual(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling sequence_equal() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.sequence_equal(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.sequence_equal(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling sequence_equal() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self.assertTrue(self._linq.sequence_equal([1, 2, 3, 4, 5]))
        self.assertFalse(self._linq.sequence_equal({}))
        self.assertTrue(self._linq.sequence_equal({1, 2, 3, 4, 5}))
        self.assertFalse(self._linq.sequence_equal("12345"))
        self.assertTrue(self._linq.sequence_equal(self._linq))
        self.assertFalse(self._linq.sequence_equal([]))
        self._linq = Linq([])
        self.assertTrue(self._linq.sequence_equal([]))
