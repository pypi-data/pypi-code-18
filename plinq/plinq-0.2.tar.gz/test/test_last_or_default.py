from test.test_base import TestBase
from plinq.linq import Linq


class TestLastOrDefault(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling last_or_default() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            self._linq.last_or_default(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling last_or_default() with a callable will not raise a TypeError
        """
        # Predicate is optional, so it can be missing or None
        self.assertEqual(self._linq.last_or_default(), 5)
        self.assertEqual(self._linq.last_or_default(None, -1), 5)
        self.assertEqual(self._linq.last_or_default(self._predicate), 4)

    def test_no_last_item(self):
        """
        Tests that if there is no item to return, last_or_default will return the given default value
        """
        self.assertIsNone(self._linq.last_or_default(lambda item, index: False))
        self._linq = Linq([])
        self.assertEqual(self._linq.last_or_default(default=-1), -1)

    def test_predicate_execution(self):
        """
        Tests that predicate will be invoked only for the needed times
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            return item % 2 == 0
        last = self._linq.last_or_default(predicate)
        self.assertEqual(last, 4)
        self.assertEqual(counter, 9)

    @staticmethod
    def _predicate(item, index):
        return item % 2 == 0
