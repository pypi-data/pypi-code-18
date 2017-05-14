import typing
import collections
from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestGroupBy(TestBase):
    def setUp(self):
        self._linq = Linq([Person("Name1", 11), Person("Name2", 12), Person("Name3", 33), Person("Name4", 44)])

    def test_invalid_parameters(self):
        """
        Tests that calling group_by() should raise a TypeError, in case parameters are not valid
        """
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector must be a callable
            self._linq.group_by(5)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector cannot be None - it is not optional
            self._linq.group_by(None)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter element_selector must be a callable
            self._linq.group_by(lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'element_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.group_by(lambda x: x, lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    def test_valid_parameters(self):
        """
        Tests that calling group_by() with valid parameters will not raise a TypeError
        """
        # Different types of callable objects
        self._linq.group_by(lambda item, index: True)
        self._linq.group_by(self._valid_key_selector)
        self._linq.group_by(self._invalid_key_selector)
        self._linq.group_by(self._valid_key_selector, self._valid_element_selector)
        self._linq.group_by(self._valid_key_selector, self._invalid_element_selector)
        self._linq.group_by(self._valid_key_selector, self._valid_element_selector, self._valid_result_selector)
        self._linq.group_by(self._valid_key_selector, self._valid_element_selector, self._invalid_result_selector)

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that using group_by with wrong parameters will raise a TypeError when iteration starts
        """
        # key_selector must have only one parameter
        group_by = self._linq.group_by(lambda x, y: True)
        with self.assertRaises(TypeError):
            for item in group_by:
                item += 1
        # element_selector must have only one parameter
        group_by = self._linq.group_by(lambda x: True, lambda x, y: -1)
        with self.assertRaises(TypeError):
            for item in group_by:
                item += 1
        # result_selector must have two parameters
        group_by = self._linq.group_by(lambda x: True, lambda x: -1, lambda key: key)
        with self.assertRaises(TypeError):
            for item in group_by:
                item += 1

    def test_iteration_with_right_parameters(self):
        """
        Tests that using group_by with the right parameters, will not raise a TypeError when iteration starts
        Tests also, that grouping takes effect
        """
        GroupByResult = collections.namedtuple("GroupByResult", ["key", "items"])
        expected_values = [GroupByResult(1, [Person("Name1", 11), Person("Name2", 12)]),
                           GroupByResult(3, [Person("Name3", 33)]),
                           GroupByResult(4, [Person("Name4", 44)])]
        # With only key_selector
        self._test_range(self._linq.group_by(self._valid_key_selector), expected_values)
        expected_values = [GroupByResult(1, ["Name1", "Name2"]),
                           GroupByResult(3, ["Name3"]),
                           GroupByResult(4, ["Name4"])]
        # With key_selector and element_selector
        self._test_range(self._linq.group_by(self._valid_key_selector, self._valid_element_selector), expected_values)
        expected_values = [(10, 20, ["Name1", "Name2"]),
                           (30, 40, ["Name3"]),
                           (40, 50, ["Name4"])]
        # With key_selector and result_selector
        self._test_range(self._linq.group_by(self._valid_key_selector,
                                              None,
                                              self._valid_result_selector),
                         expected_values)
        # With key_selector, element_selector and result_selector
        self._test_range(self._linq.group_by(self._valid_key_selector,
                                              self._valid_element_selector,
                                              lambda key, names: (key * 10, (key + 1) * 10, names)),
                         expected_values)

    def test_lazy_execution(self):
        """
        Tests that selectors will not be invoked until iterating takes place
        """
        key_selector_counter = 0
        element_selector_counter = 0
        result_selector_counter = 0

        def key_selector(person: Person):
            nonlocal key_selector_counter
            key_selector_counter += 1
            return int(person.age / 10)

        def element_selector(person: Person):
            nonlocal element_selector_counter
            element_selector_counter += 1
            return person.name

        def result_selector(key: int, names: typing.List[str]):
            nonlocal result_selector_counter
            result_selector_counter += 1
            return key * 10, (key + 1) * 10, names
        group_by_range = self._linq.group_by(key_selector, element_selector, result_selector)
        self.assertEqual(key_selector_counter, 0)
        self.assertEqual(element_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        group_by_iterator = iter(group_by_range)
        self.assertEqual(key_selector_counter, 0)
        self.assertEqual(element_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        self.assertEqual((10, 20, ["Name1", "Name2"]), next(group_by_iterator))
        self.assertEqual(key_selector_counter, 4)
        self.assertEqual(element_selector_counter, 4)
        self.assertEqual(result_selector_counter, 1)
        self.assertEqual((30, 40, ["Name3"]), next(group_by_iterator))
        self.assertEqual(key_selector_counter, 4)
        self.assertEqual(element_selector_counter, 4)
        self.assertEqual(result_selector_counter, 2)
        self.assertEqual((40, 50, ["Name4"]), next(group_by_iterator))
        self.assertEqual(key_selector_counter, 4)
        self.assertEqual(element_selector_counter, 4)
        self.assertEqual(result_selector_counter, 3)

    @staticmethod
    def _valid_key_selector(person: Person):
        return int(person.age / 10)

    @staticmethod
    def _invalid_key_selector(item: typing.Any, index: int):
        index += 1
        return item

    @staticmethod
    def _valid_element_selector(person: Person):
        return person.name

    @staticmethod
    def _invalid_element_selector(item: typing.Any, index: int):
        index += 1
        return item

    @staticmethod
    def _valid_result_selector(key: int, people: typing.List[Person]):
        return key * 10, (key + 1) * 10, [person.name for person in people]

    @staticmethod
    def _invalid_result_selector(key: typing.Any):
        return key
