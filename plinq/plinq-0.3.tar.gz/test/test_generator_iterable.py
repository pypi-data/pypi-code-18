from unittest import TestCase
from plinq.generator_iterable import GeneratorIterable


class TestGeneratorIterable(TestCase):
    def test_invalid_parameters(self):
        """
        Tests that creating GeneratorIterable should raise a TypeError, in case generator is not callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter generator must be a callable
            GeneratorIterable(5)
        self.assertEqual(str(context.exception), "Parameter 'generator' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter generator cannot be None - it is not optional
            GeneratorIterable(None)
        self.assertEqual(str(context.exception), "Parameter 'generator' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that creating GeneratorIterable with a callable will not raise a TypeError
        """
        # Different types of callable objects as generator
        GeneratorIterable(lambda item, index: True)
        GeneratorIterable(self._simple_generator)
        GeneratorIterable(self._mixed_generator)
        GeneratorIterable(self._generator_with_keyword_arguments)
        GeneratorIterable(self._generator_with_positional_arguments)

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that creating GeneratorIterable with wrong generator will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # generator must be a real generator, not just any callable
            for item in GeneratorIterable(lambda x: True):
                item += 1
        with self.assertRaises(TypeError):
            # Generator must be able to handle the arguments passed to GeneratorIterable
            for item in GeneratorIterable(self._generator_with_positional_arguments, 1, 2, 3):
                item += 1

    def test_iteration_with_right_parameters(self):
        """
        Tests that creating and using GeneratorIterable with the right parameters,
        will not raise a TypeError when iteration starts
        Tests also, that returned values are correct
        """
        generator_iterable = GeneratorIterable(self._simple_generator)
        expected_values = [0, 1, 2, 3, 4]
        for actual_value, expected_value in zip(generator_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)
        generator_iterable = GeneratorIterable(self._generator_with_positional_arguments, 5, 6)
        expected_values = [(5, 6), (5, 6), (5, 6), (5, 6), (5, 6)]
        for actual_value, expected_value in zip(generator_iterable, expected_values):
            self.assertEqual(actual_value, expected_value)
        generator_iterable = GeneratorIterable(self._generator_with_keyword_arguments, a=1, b=2, c=3)
        # Since keyword arguments are basically a dictionary, which has no fixed order,
        # it is better to create a set from the iterable, and compare it with an other set of expected values
        expected_values = {("a", 1), ("b", 2), ("c", 3)}
        self.assertEqual(set(generator_iterable), expected_values)
        generator_iterable = GeneratorIterable(self._mixed_generator, 1, 2, 3, a=1, b=2, c=3)
        expected_values = {1, 2, 3, ("a", 1), ("b", 2), ("c", 3)}
        self.assertEqual(set(generator_iterable), expected_values)

    def test_lazy_execution(self):
        """
        Tests that creating a GeneratorIterable will invoke the generator until iterating takes place
        """
        counter = 0

        def generator():
            nonlocal counter
            for i in range(5):
                counter += 1
                yield i

        generator_iterable = GeneratorIterable(generator)
        self.assertEqual(counter, 0)
        generator_iterator = iter(generator_iterable)
        self.assertEqual(counter, 0)
        self.assertEqual(0, next(generator_iterator))
        self.assertEqual(counter, 1)
        self.assertEqual(1, next(generator_iterator))
        self.assertEqual(counter, 2)
        self.assertEqual(2, next(generator_iterator))
        self.assertEqual(counter, 3)
        self.assertEqual(3, next(generator_iterator))
        self.assertEqual(counter, 4)
        self.assertEqual(4, next(generator_iterator))
        self.assertEqual(counter, 5)
        # Make sure there are no more elements in the iterator
        with self.assertRaises(StopIteration):
            next(generator_iterator)

    @staticmethod
    def _simple_generator():
        for i in range(5):
            yield i

    @staticmethod
    def _generator_with_positional_arguments(a, b):
        for i in range(5):
            yield a, b

    @staticmethod
    def _generator_with_keyword_arguments(**kwargs):
        for i in kwargs:
            yield i, kwargs[i]

    @staticmethod
    def _mixed_generator(*args, **kwargs):
        for i in args:
            yield i
        for i in kwargs:
            yield i, kwargs[i]
