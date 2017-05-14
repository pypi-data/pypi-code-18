from test.test_base import TestBase


class TestSkipWhile(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling skip_while() should raise a TypeError, in case predicate is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter predicate must be a callable
            self._linq.skip_while(5)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter predicate cannot be None - it is not optional
            self._linq.skip_while(None)
        self.assertEqual(str(context.exception), "Parameter 'predicate' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling skip_while() with a callable will not raise a TypeError
        """
        # Different types of callable objects as predicates
        self._linq.skip_while(lambda item, index: True)
        self._linq.skip_while(self._predicate_with_parameters)
        self._linq.skip_while(self._predicate_with_keyword_arguments)

    def test_iteration_with_wrong_predicate(self):
        """
        Tests that using skip_while with wrong predicate will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Predicate must have two parameters
            for item in self._linq.skip_while(lambda x: True):
                item += 1
        with self.assertRaises(TypeError):
            # Predicate must have positional arguments, not keyword ones
            for item in self._linq.skip_while(self._predicate_with_keyword_arguments):
                item += 1

    def test_iteration_with_right_predicate(self):
        """
        Tests that using skip_while with the right predicate, will not raise a TypeError when iteration starts
        Tests also, that predicate takes effect
        """
        self._test_range(self._linq.skip_while(lambda item, index: True), [])
        self._test_range(self._linq.skip_while(lambda item, index: False), [1, 2, 3, 4, 5])
        self._test_range(self._linq.skip_while(self._predicate_with_parameters), [4, 5])

    def test_lazy_execution(self):
        """
        Tests that predicate will not be invoked until iterating takes place
        """
        counter = 0

        def predicate(item, index):
            nonlocal counter
            counter += 1
            index += 1
            return item < 4
        skip_range = self._linq.skip_while(predicate)
        self.assertEqual(counter, 0)
        skip_iterator = iter(skip_range)
        self.assertEqual(counter, 0)
        self.assertEqual(4, next(skip_iterator))
        self.assertEqual(counter, 4)
        self.assertEqual(5, next(skip_iterator))
        self.assertEqual(counter, 4)

    @staticmethod
    def _predicate_with_parameters(item, index: int):
        index += 1
        return item < 4

    @staticmethod
    def _predicate_with_keyword_arguments(**kwargs):
        return kwargs["item"] % 2 == 0
