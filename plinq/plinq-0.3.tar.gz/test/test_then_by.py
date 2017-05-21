from test.test_base import TestBase
from plinq.linq import OrderedLinq
from plinq.ordered_iterable import OrderedIterable
from plinq.ordered_iterable import OrderOption
from test.utils import Person


class TestThenBy(TestBase):
    def setUp(self):
        items = [("C", 3), ("C", 2), ("C", 1), ("B", 3), ("B", 2), ("B", 1), ("A", 3), ("A", 2), ("A", 1)]
        # By default the list is ordered by the first item in the tuples
        ordered_items = OrderedIterable(items, OrderOption(lambda x: x[0]))
        self._linq = OrderedLinq(ordered_items)

    def test_invalid_parameters(self):
        """
        Tests that calling then_by() should raise a TypeError, in case key_selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector must be a callable
            self._linq.then_by(5)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling then_by() with a callable or none will not raise a TypeError
        """
        # Different types of callable objects as key_selectors
        self._linq.then_by(lambda item, index: True)
        self._linq.then_by(self._key_selector)
        # None works too, since key_Selector is optional
        self._linq.then_by(None)
        self._linq.then_by()

    def test_iteration_with_wrong_key_selector(self):
        """
        Tests that using then_by with wrong key_selector will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # key_selector must have only one parameter
            for item in self._linq.then_by(lambda x, y: True):
                item += 1
        with self.assertRaises(TypeError):
            # key_selector must have positional argument
            for item in self._linq.then_by(lambda **kwargs: True):
                item += 1

    def test_iteration_with_right_key_selector(self):
        """
        Tests that using then_by with the right key_selector, will not raise a TypeError when iteration starts
        Tests also, that ordering takes effect
        """
        expected_values = [("A", 1), ("A", 2), ("A", 3), ("B", 1), ("B", 2), ("B", 3), ("C", 1), ("C", 2), ("C", 3)]
        self._test_range(self._linq.then_by(lambda x: x), expected_values)
        # OrderedLinq is designed in a way, that subsequent then_by calls have a chaining effect
        # so we need to reset the self._linq member before every call
        self.setUp()
        self._test_range(self._linq.then_by(self._key_selector), expected_values)
        self.setUp()
        expected_values = [("A", 3), ("A", 2), ("A", 1), ("B", 3), ("B", 2), ("B", 1), ("C", 3), ("C", 2), ("C", 1)]
        self._test_range(self._linq.then_by(lambda x: -x[1]), expected_values)
        people = [Person("Name3", 55), Person("Name2", 44), Person("Name1", 44)]
        ordered_people = OrderedIterable(people, OrderOption(lambda person: person.age))
        self._linq = OrderedLinq(ordered_people)
        expected_values = [Person("Name1", 44), Person("Name2", 44), Person("Name3", 55)]
        self._test_range(self._linq.then_by(lambda p: p.name), expected_values)

    def test_lazy_execution(self):
        """
        Tests that key_selector will not be invoked until iterating takes place
        """
        counter = 0

        def key_selector(item):
            nonlocal counter
            counter += 1
            return item
        then_by_range = self._linq.then_by(key_selector)
        expected_values = [("A", 1), ("A", 2), ("A", 3), ("B", 1), ("B", 2), ("B", 3), ("C", 1), ("C", 2), ("C", 3)]
        self.assertEqual(counter, 0)
        then_by_iterator = iter(then_by_range)
        self.assertEqual(counter, 0)
        self.assertEqual(expected_values[0], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[1], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[2], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[3], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[4], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[5], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[6], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[7], next(then_by_iterator))
        self.assertEqual(counter, 9)
        self.assertEqual(expected_values[8], next(then_by_iterator))
        self.assertEqual(counter, 9)
        # Make sure there are no more elements in the iterator
        with self.assertRaises(StopIteration):
            next(then_by_iterator)

    @staticmethod
    def _key_selector(item):
        return item
