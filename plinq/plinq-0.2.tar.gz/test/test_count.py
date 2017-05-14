from test.test_base import TestBase
from plinq.linq import Linq


class TestCount(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling count() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter predicate must be a callable
            self._linq.count(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling count() with a callable will not raise a TypeError
        """
        # Different types of callable objects as predicates
        self._linq.count(lambda item, index: True)
        self._linq.count(self._predicate_with_parameters)
        # Predicate is optional, so it can be either None or can be missing at all
        self._linq.count(None)
        self._linq.count()

    def test_iteration_with_wrong_predicate(self):
        """
        Tests that using count with wrong predicate will raise a TypeError
        """
        with self.assertRaises(TypeError):
            # Predicate must have two parameters
            self._linq.count(lambda x: True)
        with self.assertRaises(TypeError):
            # Predicate must have positional arguments, not keyword ones
            self._linq.count(self._predicate_with_keyword_arguments)

    def test_iteration_with_right_predicate(self):
        """
        Tests that using count with the right predicate, will not raise a TypeError
        Tests also, that count returns the right value takes effect
        """
        iterable = []
        self.assertEqual(5, self._linq.count(lambda item, index: True))
        self.assertEqual(5, self._linq.count())
        self.assertEqual(0, self._linq.count(lambda item, index: False))
        self.assertEqual(2, self._linq.count(self._predicate_with_parameters))
        self._linq = Linq(iterable)
        self.assertEqual(0, self._linq.count(lambda item, index: True))
        self.assertEqual(0, self._linq.count())
        self.assertEqual(0, self._linq.count(lambda item, index: False))
        self.assertEqual(0, self._linq.count(self._predicate_with_parameters))
        iterable.append(1)
        self.assertEqual(1, self._linq.count(lambda item, index: True))
        self.assertEqual(1, self._linq.count())

    def test_predicate_execution(self):
        """
        Tests that predicate will be invoked for each element
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            return item % 2 == 0
        count = self._linq.count(predicate)
        self.assertEqual(counter, 5)
        self.assertEqual(count, 2)
        counter = 0
        self._linq = Linq([])
        count = self._linq.count(predicate)
        self.assertEqual(counter, 0)
        self.assertEqual(count, 0)

    @staticmethod
    def _predicate_with_parameters(item, index: int):
        index += 1
        return item % 2 == 0

    @staticmethod
    def _predicate_with_keyword_arguments(**kwargs):
        return kwargs["item"] % 2 == 0
