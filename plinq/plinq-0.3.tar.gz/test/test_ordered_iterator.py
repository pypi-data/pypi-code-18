from unittest import TestCase
from plinq.ordered_iterable import OrderedIterator
from plinq.ordered_iterable import OrderOption
from test.utils import ValidIteratorIterable
from test.utils import IntIteratorIterable
from test.utils import Person


class TestOrderedIterator(TestCase):
    def test_invalid_parameters(self):
        """
        Tests that creating an OrderedIterator should raise a TypeError, in case iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            OrderedIterator(5, [])
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            OrderedIterator(IntIteratorIterable(), [])
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            OrderedIterator(None, None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that creating OrderedIterator with an iterable will not raise a TypeError
        """
        # Different types of iterable objects as iterable
        OrderedIterator([], None)
        OrderedIterator({}, [])
        OrderedIterator(set(), [])
        OrderedIterator(ValidIteratorIterable(), [])

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that creating OrderedIterator with wrong parameters will raise a AttributeError when iteration starts
        """
        with self.assertRaises(AttributeError):
            # order_options must be a list of OrderOption objects
            for item in OrderedIterator([1, 2, 3], [1, 2, 3]):
                item += 1

    def test_iteration_with_right_parameters(self):
        """
        Tests that creating and using OrderedIterator with the right parameters,
        will not raise any error when iteration starts
        Tests also, that returned values are correct
        """
        ordered_iterator = OrderedIterator([1, 2, 3, 4, 5], [])
        expected_values = [1, 2, 3, 4, 5]
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterator = OrderedIterator([1, 2, 3, 4, 5], [OrderOption(lambda x: x)])
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterator = OrderedIterator([1, 2, 3, 4, 5], [OrderOption(lambda x: x, reverse=True)])
        expected_values = [5, 4, 3, 2, 1]
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterator = OrderedIterator([Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)],
                                           [OrderOption(lambda p: p.name)])
        expected_values = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
            self.assertEqual(actual_value, expected_value)

        ordered_iterator = OrderedIterator([Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)],
                                           [OrderOption(lambda p: p.name, reverse=True)])
        expected_values = [Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)]
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
            self.assertEqual(actual_value, expected_value)
        ordered_iterator = OrderedIterator([Person("Name3", 33), Person("Name3", 34),
                                            Person("Name2", 22), Person("Name2", 23),
                                            Person("Name1", 11), Person("Name1", 12)],
                                           [OrderOption(lambda p: p.age, reverse=True), OrderOption(lambda p: p.name)])
        expected_values = [Person("Name1", 12), Person("Name1", 11),
                           Person("Name2", 23), Person("Name2", 22),
                           Person("Name3", 34), Person("Name3", 33)]
        for actual_value, expected_value in zip(ordered_iterator, expected_values):
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

        ordered_iterator = OrderedIterator([Person("Name3", 33), Person("Name2", 22), Person("Name1", 11)],
                                           [OrderOption(key_selector)])
        expected_values = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self.assertEqual(counter, 0)
        iterator = iter(ordered_iterator)
        self.assertEqual(counter, 0)
        self.assertEqual(expected_values[0], next(iterator))
        self.assertEqual(counter, 3)
        self.assertEqual(expected_values[1], next(iterator))
        self.assertEqual(counter, 3)
        self.assertEqual(expected_values[2], next(iterator))
        self.assertEqual(counter, 3)
        # Make sure there are no more elements in the iterator
        with self.assertRaises(StopIteration):
            next(iterator)
