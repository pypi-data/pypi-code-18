from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestSelect(TestBase):
    def setUp(self):
        people = [Person("Name1", 11, [11]), Person("Name2", 22, [22]), Person("Name3", 33, [33])]
        self._linq = Linq(people)

    def test_invalid_parameters(self):
        """
        Tests that calling select() should raise a TypeError, in case selector is not a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter selector must be a callable
            self._linq.select(5)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter selector cannot be None - it is not optional
            self._linq.select(None)
        self.assertEqual(str(context.exception), "Parameter 'selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling select() with a callable will not raise a TypeError
        """
        # Different types of callable objects as selectors
        self._linq.select(lambda item, index: True)
        self._linq.select(self._selector_with_parameters)
        self._linq.select(self._selector_with_keyword_arguments)

    def test_iteration_with_wrong_selector(self):
        """
        Tests that using select with wrong selector will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Selector must have two parameters
            for item in self._linq.select(lambda x: True):
                item += 1
        with self.assertRaises(TypeError):
            # Selector must have positional arguments, not keyword ones
            for item in self._linq.select(self._selector_with_keyword_arguments):
                item += 1

    def test_iteration_with_right_selector(self):
        """
        Tests that using select with the right selector, will not raise a TypeError when iteration starts
        Tests also, that selector takes effect
        """
        self._test_range(self._linq.select(lambda item, index: item.name), ["Name1", "Name2", "Name3"])
        self._test_range(self._linq.select(lambda item, index: index + 1), [1, 2, 3])
        self._test_range(self._linq.select(self._selector_with_parameters), ["Name1", "Name2", "Name3"])

    def test_lazy_execution(self):
        """
        Tests that selector will not be invoked until iterating takes place
        """
        counter = 0

        def selector(item, index):
            nonlocal counter
            counter += 1
            index += 1
            return item.name
        select_range = self._linq.select(selector)
        self.assertEqual(counter, 0)
        select_iterator = iter(select_range)
        self.assertEqual(counter, 0)
        self.assertEqual("Name1", next(select_iterator))
        self.assertEqual(counter, 1)
        self.assertEqual("Name2", next(select_iterator))
        self.assertEqual(counter, 2)
        self.assertEqual("Name3", next(select_iterator))
        self.assertEqual(counter, 3)

    @staticmethod
    def _selector_with_parameters(item: Person, index: int):
        index += 1
        return item.name

    @staticmethod
    def _selector_with_keyword_arguments(**kwargs):
        return kwargs["index"] + 1
