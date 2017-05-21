from unittest import TestCase
from plinq.ordered_iterable import OrderedIterable
from plinq.ordered_iterable import OrderOption
from test.utils import ValidIteratorIterable
from test.utils import IntIteratorIterable
from test.utils import Person


class TestOrderedIterable(TestCase):
    def test_invalid_parameters(self):
        """
        Tests that creating an OrderedIterable should raise a TypeError, in case iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            OrderedIterable(5, OrderOption(lambda x: x))
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            OrderedIterable(IntIteratorIterable(), OrderOption(lambda x: x))
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            OrderedIterable(None, OrderOption(lambda x: x))
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter order_option must be an OrderOption
            OrderedIterable([], 5)
        self.assertEqual(str(context.exception), "Parameter 'order_option' must be an OrderOption object")
        with self.assertRaises(TypeError) as context:
            # Parameter order_option cannot be None - it is not optional
            OrderedIterable([], 5)
        self.assertEqual(str(context.exception), "Parameter 'order_option' must be an OrderOption object")

    def test_valid_parameters(self):
        """
        Tests that creating OrderedIterable with an iterable will not raise a TypeError
        """
        # Different types of iterable objects as iterable
        OrderedIterable([], OrderOption(lambda x: x))
        OrderedIterable({}, OrderOption(lambda x: x))
        OrderedIterable(set(), OrderOption(lambda x: x))
        OrderedIterable(ValidIteratorIterable(), OrderOption(lambda x: x))

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that creating OrderedIterable with wrong parameters will raise a AttributeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # order_option must be an OrderOption object
            for item in OrderedIterable([1, 2, 3], 1):
                item += 1

    def test_iteration_with_right_parameters(self):
        """
        Tests that creating and using OrderedIterable with the right parameters,
        will not raise any error when iteration starts
        Tests also, that returned values are correct
        """
        ordered_iterable = OrderedIterable([1, 2, 3, 4, 5], OrderOption(lambda x: x))
        expected_values = [1, 2, 3, 4, 5]
        for actual_value, expected_value in zip(ordered_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterable = OrderedIterable([1, 2, 3, 4, 5], OrderOption(lambda x: x, reverse=True))
        expected_values = [5, 4, 3, 2, 1]
        for actual_value, expected_value in zip(ordered_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterable = OrderedIterable([Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)],
                                           OrderOption(lambda p: p.name))
        expected_values = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        for actual_value, expected_value in zip(ordered_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)

        ordered_iterable = OrderedIterable([Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)],
                                           OrderOption(lambda p: p.name, reverse=True))
        expected_values = [Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)]
        for actual_value, expected_value in zip(ordered_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)

        ordered_iterable = OrderedIterable([Person("Name3", 33), Person("Name3", 34),
                                            Person("Name2", 22), Person("Name2", 23),
                                            Person("Name1", 11), Person("Name1", 12)],
                                           OrderOption(lambda p: p.name))
        ordered_iterable.add_order(OrderOption(lambda p: p.age, reverse=True))
        expected_values = [Person("Name1", 12), Person("Name1", 11),
                           Person("Name2", 23), Person("Name2", 22),
                           Person("Name3", 34), Person("Name3", 33)]
        for actual_value, expected_value in zip(ordered_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)

    def test_lazy_execution(self):
        """
        Tests that creating a GeneratorIterable will invoke the generator until iterating takes place
        """
        counter = 0

        def key_selector(person):
            nonlocal counter
            counter += 1
            return person.name

        ordered_iterable = OrderedIterable([Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)],
                                           OrderOption(key_selector))
        expected_values = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self.assertEqual(counter, 0)
        ordered_iterator = iter(ordered_iterable)
        self.assertEqual(counter, 0)
        self.assertEqual(expected_values[0], next(ordered_iterator))
        self.assertEqual(counter, 3)
        self.assertEqual(expected_values[1], next(ordered_iterator))
        self.assertEqual(counter, 3)
        self.assertEqual(expected_values[2], next(ordered_iterator))
        self.assertEqual(counter, 3)
        # Make sure there are no more elements in the iterator
        with self.assertRaises(StopIteration):
            next(ordered_iterator)
