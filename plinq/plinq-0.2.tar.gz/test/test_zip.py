from test.test_base import TestBase


class TestZip(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling zip() should raise a TypeError, in case parameters are not valid
        """
        self._test_invalid_inner_iterable_parameters()
        self._test_invalid_result_selector_parameters()

    def test_valid_parameters(self):
        """
        Tests that calling zip() with right parameters will not raise a TypeError 
        """
        # Different types of callable objects as predicates
        self._linq.zip([], lambda x: x)
        self._linq.zip([], self._valid_result_selector)
        self._linq.zip([], self._invalid_result_selector)

    def test_iteration_with_wrong_selector(self):
        """
        Tests that using zip with wrong selector will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # result_selector must have two parameters
            for item in self._linq.zip(lambda x: True):
                item += 1
                pass
        with self.assertRaises(TypeError):
            # result_selector must have two parameters - and they cannot be keyword arguments
            for item in self._linq.zip(lambda **kwargs: True):
                item += 1
                pass

    def test_iteration_with_right_selector(self):
        """
        Tests that using zip with the right selector, will not raise a TypeError when iteration starts
        Tests also, that selector takes effect
        """
        expected_values = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        self._test_range(self._linq.zip([1, 2, 3, 4, 5, 6, 7], lambda x, y: (x, y)), expected_values)
        expected_values = [(1, 1.0), (2, 2.0)]
        self._test_range(self._linq.zip([1.0, 2.0], lambda x, y: (x, y)), expected_values)
        expected_values = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
        self._test_range(self._linq.zip(["1", "2", "3", "4", "5"], self._valid_result_selector), expected_values)
        expected_values = []
        self._test_range(self._linq.zip([], self._valid_result_selector), expected_values)

    def test_lazy_execution(self):
        """
        Tests that selector will not be invoked until iterating takes place
        """
        counter = 0

        def selector(outer_item, inner_item):
            nonlocal counter
            counter += 1
            return outer_item, inner_item
        zip_range = self._linq.zip(["1", "2", "3", "4", "5"], selector)
        self.assertEqual(counter, 0)
        zip_iterator = iter(zip_range)
        self.assertEqual(counter, 0)
        self.assertEqual((1, "1"), next(zip_iterator))
        self.assertEqual(counter, 1)
        self.assertEqual((2, "2"), next(zip_iterator))
        self.assertEqual(counter, 2)
        self.assertEqual((3, "3"), next(zip_iterator))
        self.assertEqual(counter, 3)
        self.assertEqual((4, "4"), next(zip_iterator))
        self.assertEqual(counter, 4)
        self.assertEqual((5, "5"), next(zip_iterator))
        self.assertEqual(counter, 5)

    def _test_invalid_inner_iterable_parameters(self):
        """
        Helper method to test if invalid inner_iterable parameters causes TypeError when zip() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable must be iterable
            self._linq.zip(5, lambda x, y: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable cannot be None - it is not optional
            self._linq.zip(None, lambda x, y: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")

    def _test_invalid_result_selector_parameters(self):
        """
        Helper method to test if invalid result_selector parameters causes TypeError when zip() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.zip([], 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    @staticmethod
    def _valid_result_selector(outer_item, inner_item):
        return outer_item, inner_item

    def _invalid_result_selector(self, **kwargs):
        pass
