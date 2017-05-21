from test.test_base import TestBase
from plinq.linq import Linq


class TestFirst(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling first() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            self._linq.first(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling first() with a callable will not raise a TypeError
        """
        # Predicate is optional, so it can be missing or None
        self.assertEqual(self._linq.first(), 1)
        self.assertEqual(self._linq.first(None), 1)
        self.assertEqual(self._linq.first(self._predicate), 2)

    def test_no_first_item(self):
        """
        Tests that if there is no item to return, first raises an IndexError
        """
        with self.assertRaises(IndexError):
            self._linq.first(lambda item, index: False)
        self._linq = Linq([])
        with self.assertRaises(IndexError):
            self._linq.first()

    def test_predicate_execution(self):
        """
        Tests that predicate will be invoked only for the needed times
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            return item % 2 == 0
        first = self._linq.first(predicate)
        self.assertEqual(first, 2)
        self.assertEqual(counter, 2)

    @staticmethod
    def _predicate(item, index):
        return item % 2 == 0
