from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestOrderByDescending(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling order_by_descending() should raise a TypeError, in case key_selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector must be a callable
            self._linq.order_by_descending(5)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling order_by_descending() with a callable or none will not raise a TypeError
        """
        # Different types of callable objects as key_selectors
        self._linq.order_by_descending(lambda item, index: True)
        self._linq.order_by_descending(self._key_selector)
        # None works too, since key_Selector is optional
        self._linq.order_by_descending(None)
        self._linq.order_by_descending()

    def test_iteration_with_wrong_key_selector(self):
        """
        Tests that using order_by_descending with wrong key_selector will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # key_selector must have only one parameter
            for item in self._linq.order_by_descending(lambda x, y: True):
                item += 1
        with self.assertRaises(TypeError):
            # key_selector must have positional argument
            for item in self._linq.order_by_descending(lambda **kwargs: True):
                item += 1

    def test_iteration_with_right_key_selector(self):
        """
        Tests that using order_by_descending with the right key_selector,
        will not raise a TypeError when iteration starts
        Tests also, that ordering takes effect
        """
        self._test_range(self._linq.order_by_descending(lambda x: x), [5, 4, 3, 2, 1])
        self._test_range(self._linq.order_by_descending(self._key_selector), [5, 4, 3, 2, 1])
        self._test_range(self._linq.order_by_descending(lambda x: -x), [1, 2, 3, 4, 5])
        self._linq = Linq([Person("Name1", 55, []), Person("Name2", 44, []), Person("Name3", 33, [])])
        expected_values = [Person("Name1", 55, []), Person("Name2", 44, []), Person("Name3", 33, [])]
        self._test_range(self._linq.order_by_descending(lambda p: p.age), expected_values)

    def test_lazy_execution(self):
        """
        Tests that key_selector will not be invoked until iterating takes place
        """
        counter = 0

        def key_selector(item):
            nonlocal counter
            counter += 1
            return item
        order_by_range = self._linq.order_by_descending(key_selector)
        self.assertEqual(counter, 0)
        order_by_iterator = iter(order_by_range)
        self.assertEqual(counter, 0)
        self.assertEqual(5, next(order_by_iterator))
        self.assertEqual(counter, 5)
        self.assertEqual(4, next(order_by_iterator))
        self.assertEqual(counter, 5)
        self.assertEqual(3, next(order_by_iterator))
        self.assertEqual(counter, 5)
        self.assertEqual(2, next(order_by_iterator))
        self.assertEqual(counter, 5)
        self.assertEqual(1, next(order_by_iterator))
        self.assertEqual(counter, 5)

    @staticmethod
    def _key_selector(item):
        return item
