from plinq.linq import Linq
from test.test_base import TestBase


class TestOfType(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling of_type() should raise a TypeError, in case of_type parameter is not a type
        """
        with self.assertRaises(TypeError) as context:
            # Parameter of_type must be a type
            self._linq.of_type(5)
        self.assertEqual(str(context.exception), "Parameter 'of_type' must be a type")

    def test_valid_parameters(self):
        """
        Tests that calling of_type() with a type will not raise a TypeError
        """
        # Different types as of_type
        self._linq.of_type(int)
        self._linq.of_type(float)
        self._linq.of_type(str)

    def test_iteration(self):
        """
        Tests that using of_type with a right of_type parameter, will not raise a TypeError when iteration starts
        Tests also, that of_type takes effect
        """
        self._test_range(self._linq.of_type(int), [1, 2, 3, 4, 5])
        self._test_range(self._linq.of_type(float), [])
        self._linq = Linq([1, 2.0, 3, 4.0, 5])
        self._test_range(self._linq.of_type(float), [2.0, 4.0])
        self._test_range(self._linq.of_type(int), [1, 3, 5])
