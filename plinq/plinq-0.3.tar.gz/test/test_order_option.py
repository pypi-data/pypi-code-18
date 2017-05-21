from unittest import TestCase
from plinq.ordered_iterable import OrderOption


class TestOrderOption(TestCase):
    def test_invalid_parameters(self):
        """
        Tests that creating OrderOption should raise a TypeError, in case key_selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector must be a callable
            OrderOption(5)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that creating OrderOption with a callable will not raise a TypeError
        """
        # Different types of callable objects as generator
        OrderOption(lambda item: True)
        OrderOption(self._key_selector)

    def test_members(self):
        """
        Tests that creating OrderOption will store the provided parameters
        """
        order_option = OrderOption(self._key_selector)
        self.assertEqual(order_option.key_selector, self._key_selector)
        self.assertFalse(order_option.reverse)
        order_option = OrderOption(self._key_selector, reverse=True)
        self.assertEqual(order_option.key_selector, self._key_selector)
        self.assertTrue(order_option.reverse)

    @staticmethod
    def _key_selector(item):
        return item
