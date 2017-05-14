from test.test_base import TestBase
from plinq.linq import Linq


class TestAggregate(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling aggregate() should raise a TypeError, in case parameters are not callables
        """
        with self.assertRaises(TypeError) as context:
            # Parameter accumulator must be a callable
            self._linq.aggregate(5)
        self.assertEqual(str(context.exception), "Parameter 'accumulator' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter accumulator cannot be None - it is not optional
            self._linq.aggregate(None)
        self.assertEqual(str(context.exception), "Parameter 'accumulator' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.aggregate(lambda x: x, result_selector=5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling aggregate() with the right parameters will not raise a TypeError
        """
        # Calculate sum
        self.assertEqual(self._linq.aggregate(lambda x, y: x + y), 15)
        # Find the biggest number in the range
        self.assertEqual(self._linq.aggregate(self._accumulator), 5)
        # Calculate sum of even numbers
        self.assertEqual(self._linq.aggregate(lambda x, y: x + y if y % 2 == 0 else x, 0), 6)
        # Calculate sum of odd numbers
        self.assertEqual(self._linq.aggregate(lambda x, y: x + y if y % 2 else x, 0, lambda x: str(x)), "9")

    def test_empty_range(self):
        """
        Tests that using aggregate with empty range will raise a ValueError
        """
        self._linq = Linq([])
        with self.assertRaises(ValueError) as context:
            self._linq.aggregate(lambda x, y: x)
        self.assertEqual(str(context.exception), "Operator 'aggregate' cannot work on empty range")

    @staticmethod
    def _accumulator(x: int, y: int) -> int:
        if y > x:
            return y
        return x
