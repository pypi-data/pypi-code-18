from test.test_base import TestBase
from plinq.linq import Linq


class TestSingleOrDefault(TestBase):
    def setUp(self):
        self._linq = Linq([2])

    def test_invalid_parameters(self):
        """
        Tests that calling single_or_default() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            self._linq.single_or_default(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling single_or_default() with a callable will not raise a TypeError
        """
        # Predicate is optional, so it can be missing or None
        self.assertEqual(self._linq.single_or_default(default=-1), 2)
        self.assertEqual(self._linq.single_or_default(None, default=None), 2)
        self.assertEqual(self._linq.single_or_default(self._predicate), 2)

    def test_no_single_item(self):
        """
        Tests that if there is no item to return, single_or_default will not raise an IndexError
        """
        self.assertIsNone(self._linq.single_or_default(lambda item, index: False))
        self._linq = Linq([1])
        self.assertIsNone(self._linq.single_or_default(self._predicate))
        self._linq = Linq([])
        self.assertEqual(self._linq.single_or_default(default=-1), -1)

    def test_multiple_item(self):
        """
        Tests that if there are multiple items to return, single will raise an index error
        """
        self._linq = Linq([1, 2, 3, 4, 5])
        self.assertEqual(self._linq.single_or_default(lambda item, index: item % 2 == 0, default=-1), -1)
        self.assertIsNone(self._linq.single_or_default())

    def test_predicate_execution(self):
        """
        Tests that predicate will be invoked only for the needed times
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            return item % 2 == 0
        self._linq = Linq([1, 2, 3])
        single = self._linq.single_or_default(predicate)
        self.assertEqual(single, 2)
        self.assertEqual(counter, 5)

    @staticmethod
    def _predicate(item, index):
        return item % 2 == 0
