from test.test_base import TestBase


class TestWhere(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling where() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter predicate must be a callable
            self._linq.where(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter predicate cannot be None - it is not optional
            self._linq.where(None)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling where() with a callable will not raise a TypeError
        """
        # Different types of callable objects as predicates
        self._linq.where(lambda item, index: True)
        self._linq.where(self._predicate_with_parameters)
        self._linq.where(self._predicate_with_keyword_arguments)

    def test_iteration_with_wrong_predicate(self):
        """
        Tests that using where with wrong predicate will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Predicate must have two parameters
            for item in self._linq.where(lambda x: True):
                item += 1
        with self.assertRaises(TypeError):
            # Predicate must have positional arguments, not keyword ones
            for item in self._linq.where(self._predicate_with_keyword_arguments):
                item += 1

    def test_iteration_with_right_predicate(self):
        """
        Tests that using where with the right predicate, will not raise a TypeError when iteration starts
        Tests also, that predicate takes effect
        """
        self._test_range(self._linq.where(lambda item, index: True), [1, 2, 3, 4, 5])
        self._test_range(self._linq.where(lambda item, index: False), [])
        self._test_range(self._linq.where(self._predicate_with_parameters), [2, 4])

    def test_lazy_execution(self):
        """
        Tests that predicate will not be invoked until iterating takes place
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            index += 1
            return item % 2 == 0
        where_range = self._linq.where(predicate)
        self.assertEqual(counter, 0)
        where_iterator = iter(where_range)
        self.assertEqual(counter, 0)
        self.assertEqual(2, next(where_iterator))
        self.assertEqual(counter, 2)
        self.assertEqual(4, next(where_iterator))
        self.assertEqual(counter, 4)

    @staticmethod
    def _predicate_with_parameters(item, index: int):
        index += 1
        return item % 2 == 0

    @staticmethod
    def _predicate_with_keyword_arguments(**kwargs):
        return kwargs["item"] % 2 == 0
