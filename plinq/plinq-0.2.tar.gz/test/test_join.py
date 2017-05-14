import typing
from test.test_base import TestBase
from test.utils import Person
from test.utils import House
from plinq.linq import Linq


class TestJoin(TestBase):
    def setUp(self):
        self._outer_iterable = [Person("Name1", 11, [11, 12]),
                                Person("Name2", 22, [21]),
                                Person("Name3", 33, [31, 32, 33])]
        self._inner_iterable = [House("Address1", "Name1"), House("Address2", "Name2")]
        self._linq = Linq(self._outer_iterable)

    def test_invalid_parameters(self):
        """
        Tests that calling join() should raise a TypeError, in case of the parameters are not correct
        """
        self._test_invalid_inner_iterable_parameter()
        self._test_invalid_outer_key_selector_parameter()
        self._test_invalid_inner_key_selector_parameter()
        self._test_invalid_result_selector_parameter()

    def test_valid_parameters(self):
        """
        Tests that calling join() with the right parameters will not raise a TypError
        """
        # Different types of callable objects as selectors
        self._linq.join([], lambda x: x, lambda x: x, lambda x: x)
        self._linq.join([],
                         self._valid_outer_key_selector,
                         self._valid_inner_key_selector,
                         self._valid_result_selector)
        self._linq.join([],
                         self._invalid_outer_key_selector,
                         self._invalid_inner_key_selector,
                         self._invalid_result_selector)

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that using join with wrong callable objects will raise a TypeError when iteration starts
        """
        self._test_invalid_outer_key_selectors()
        self._test_invalid_inner_key_selectors()
        self._test_invalid_result_selectors()

    def test_iteration_with_right_parameters(self):
        """
        Tests that using join with the right parameters, will not raise a TypeError when iteration starts
        Tests also, that operation takes effect
        """
        expected_values = [("Address1", [11, 12]), ("Address2", [21])]
        self._test_range(self._linq.join(self._inner_iterable,
                                          self._valid_outer_key_selector,
                                          self._valid_inner_key_selector,
                                          self._valid_result_selector),
                         expected_values)
        expected_values = [("Address1", 11), ("Address2", 22)]
        self._test_range(self._linq.join(self._inner_iterable,
                                          lambda person: person.name,
                                          lambda house: house.owner,
                                          lambda person, house: (house.address, person.age)),
                         expected_values)

    def test_lazy_execution(self):
        """
        Tests that selectors will not be invoked until iterating takes place
        """
        outer_key_selector_counter = 0
        inner_key_selector_counter = 0
        result_selector_counter = 0

        def outer_key_selector(person: Person) -> str:
            nonlocal outer_key_selector_counter
            outer_key_selector_counter += 1
            return person.name

        def inner_key_selector(house: House) -> str:
            nonlocal inner_key_selector_counter
            inner_key_selector_counter += 1
            return house.owner

        def result_selector(person: Person, house: House) -> typing.Tuple[str, typing.List[int]]:
            nonlocal result_selector_counter
            result_selector_counter += 1
            return house.address, person.phone_numbers
        join_range = self._linq.join(self._inner_iterable, outer_key_selector, inner_key_selector, result_selector)
        self.assertEqual(outer_key_selector_counter, 0)
        self.assertEqual(inner_key_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        join_iterator = iter(join_range)
        self.assertEqual(outer_key_selector_counter, 0)
        self.assertEqual(inner_key_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        self.assertEqual(("Address1", [11, 12]), next(join_iterator))
        self.assertEqual(outer_key_selector_counter, 1)
        self.assertEqual(inner_key_selector_counter, 2)
        self.assertEqual(result_selector_counter, 1)
        self.assertEqual(("Address2", [21]), next(join_iterator))
        self.assertEqual(outer_key_selector_counter, 2)
        self.assertEqual(inner_key_selector_counter, 4)
        self.assertEqual(result_selector_counter, 2)

    def _test_invalid_inner_iterable_parameter(self) -> None:
        """
        Helper method to test if invalid inner_iterable parameters causes TypeError when join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable must be an iterable
            self._linq.join(5, lambda x: x, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable cannot be None - it is not optional
            self._linq.join(None, lambda x: x, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")

    def _test_invalid_outer_key_selector_parameter(self):
        """
        Helper method to test if invalid outer_key_selector parameters causes TypeError when join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter outer_key_selector must be a callable
            self._linq.join([], 5, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'outer_key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter outer_key_selector cannot be None - it is not optional
            self._linq.join([], None, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'outer_key_selector' must be a 'callable' object")

    def _test_invalid_outer_key_selectors(self):
        """
        Helper method to test if seemingly valid outer_key_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter outer_key_selector must have exactly one parameter
            for item in self._linq.join(self._inner_iterable,
                                         lambda person, index: person.name,
                                         self._valid_inner_key_selector,
                                         self._valid_result_selector):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter outer_key_selector must have exactly one parameter - and it cannot be keyword argument
            for item in self._linq.join(self._inner_iterable,
                                         lambda **kwargs: kwargs["item"].name,
                                         self._valid_inner_key_selector,
                                         self._valid_result_selector):
                item += 1

    def _test_invalid_inner_key_selector_parameter(self):
        """
        Helper method to test if invalid inner_key_selector parameters causes TypeError when join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter inner_key_selector must be a callable
            self._linq.join([], lambda x: x, 5, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter inner_key_selector cannot be None - it is not optional
            self._linq.join([], lambda x: x, None, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_key_selector' must be a 'callable' object")

    def _test_invalid_inner_key_selectors(self):
        """
        Helper method to test if seemingly valid inner_key_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter inner_key_selector must have exactly one parameter
            for item in self._linq.join(self._inner_iterable,
                                         self._valid_outer_key_selector,
                                         lambda person, index: person.name,
                                         self._valid_result_selector):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter inner_key_selector must have exactly one parameter - and it cannot be keyword argument
            for item in self._linq.join(self._inner_iterable,
                                         self._valid_outer_key_selector,
                                         lambda **kwargs: kwargs["item"].name,
                                         self._valid_result_selector):
                item += 1

    def _test_invalid_result_selector_parameter(self):
        """
        Helper method to test if invalid result_selector parameters causes TypeError when join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.join([], lambda x: x, lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector cannot be None - it is not optional
            self._linq.join([], lambda x: x, lambda x: x, None)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    def _test_invalid_result_selectors(self):
        """
        Helper method to test if seemingly valid result_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter result_selector must have exactly two parameters
            for item in self._linq.join(self._inner_iterable,
                                         self._valid_outer_key_selector,
                                         self._valid_inner_key_selector,
                                         lambda x: x):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter result_selector must have exactly two parameters - and they cannot be keyword arguments
            for item in self._linq.join(self._inner_iterable,
                                         self._valid_outer_key_selector,
                                         self._valid_inner_key_selector,
                                         lambda **kwargs: None):
                item += 1

    @staticmethod
    def _valid_outer_key_selector(person: Person) -> str:
        return person.name

    @staticmethod
    def _valid_inner_key_selector(house: House) -> str:
        return house.owner

    @staticmethod
    def _valid_result_selector(person: Person, house: House) -> typing.Tuple[str, typing.List[int]]:
        return house.address, person.phone_numbers

    @staticmethod
    def _invalid_outer_key_selector(**kwargs) -> str:
        return kwargs["item"].name

    @staticmethod
    def _invalid_inner_key_selector(house: House, tmp: int) -> str:
        tmp += 1
        return house.owner

    @staticmethod
    def _invalid_result_selector() -> None:
        pass
