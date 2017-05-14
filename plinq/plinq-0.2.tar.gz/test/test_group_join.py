import typing
from test.test_join import TestJoin
from test.utils import Person
from test.utils import House
from plinq.linq import Linq


class TestGroupJoin(TestJoin):
    def setUp(self):
        self._outer_iterable = [Person("Name1", 11, [11, 12]),
                                Person("Name2", 22, [21]),
                                Person("Name3", 33, [31, 32, 33])]
        self._inner_iterable = [House("Address1", "Name1"),
                                House("Address2", "Name2"),
                                House("Address3", "Name3"),
                                House("Address4", "Name2")]
        self._linq = Linq(self._outer_iterable)

    def test_invalid_parameters(self):
        """
        Tests that calling group_join() should raise a TypeError, in case of the parameters are not correct
        """
        self._test_invalid_inner_iterable_parameter()
        self._test_invalid_outer_key_selector_parameter()
        self._test_invalid_inner_key_selector_parameter()
        self._test_invalid_result_selector_parameter()

    def test_valid_parameters(self):
        """
        Tests that calling group_join() with the right parameters will not raise a TypError
        """
        # Different types of callable objects as selectors
        self._linq.group_join([], lambda x: x, lambda x: x, lambda x: x)
        self._linq.group_join([],
                               self._valid_outer_key_selector,
                               self._valid_inner_key_selector,
                               self._valid_result_selector)
        self._linq.group_join([],
                               self._invalid_outer_key_selector,
                               self._invalid_inner_key_selector,
                               self._invalid_result_selector)

    def test_iteration_with_wrong_parameters(self):
        """
        Tests that using group_join with wrong callable objects will raise a TypeError when iteration starts
        """
        self._test_invalid_outer_key_selectors()
        self._test_invalid_inner_key_selectors()
        self._test_invalid_result_selectors()

    def test_iteration_with_right_parameters(self):
        """
        Tests that using group_join with the right parameters, will not raise a TypeError when iteration starts
        Tests also, that operation takes effect
        """
        expected_values = [("Name1", ["Address1"]),
                           ("Name2", ["Address2", "Address4"]),
                           ("Name3", ["Address3"])]
        self._test_range(self._linq.group_join(self._inner_iterable,
                                                self._valid_outer_key_selector,
                                                self._valid_inner_key_selector,
                                                self._valid_result_selector),
                         expected_values)
        expected_values = [("Name1", 1),
                           ("Name2", 2),
                           ("Name3", 1)]
        self._test_range(self._linq.group_join(self._inner_iterable,
                                                lambda person: person.name,
                                                lambda house: house.owner,
                                                lambda person, houses: (person.name, len(houses))),
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

        def result_selector(person: Person, houses: typing.List[House]) -> typing.Tuple[str, typing.List[int]]:
            nonlocal result_selector_counter
            result_selector_counter += 1
            return person.name, [house.address for house in houses]
        group_join_range = self._linq.group_join(self._inner_iterable,
                                                  outer_key_selector,
                                                  inner_key_selector,
                                                  result_selector)
        self.assertEqual(outer_key_selector_counter, 0)
        self.assertEqual(inner_key_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        group_join_iterator = iter(group_join_range)
        self.assertEqual(outer_key_selector_counter, 0)
        self.assertEqual(inner_key_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        self.assertEqual(("Name1", ["Address1"]), next(group_join_iterator))
        self.assertEqual(outer_key_selector_counter, 1)
        self.assertEqual(inner_key_selector_counter, 4)
        self.assertEqual(result_selector_counter, 1)
        self.assertEqual(("Name2", ["Address2", "Address4"]), next(group_join_iterator))
        self.assertEqual(outer_key_selector_counter, 2)
        self.assertEqual(inner_key_selector_counter, 8)
        self.assertEqual(result_selector_counter, 2)
        self.assertEqual(("Name3", ["Address3"]), next(group_join_iterator))
        self.assertEqual(outer_key_selector_counter, 3)
        self.assertEqual(inner_key_selector_counter, 12)
        self.assertEqual(result_selector_counter, 3)

    def _test_invalid_inner_iterable_parameter(self) -> None:
        """
        Helper method to test if invalid inner_iterable parameters causes TypeError when group_join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable must be an iterable
            self._linq.group_join(5, lambda x: x, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter inner_iterable cannot be None - it is not optional
            self._linq.group_join(None, lambda x: x, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_iterable' must be an 'iterable' object")

    def _test_invalid_outer_key_selector_parameter(self):
        """
        Helper method to test if invalid outer_key_selector parameters causes TypeError when group_join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter outer_key_selector must be a callable
            self._linq.group_join([], 5, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'outer_key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter outer_key_selector cannot be None - it is not optional
            self._linq.group_join([], None, lambda x: x, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'outer_key_selector' must be a 'callable' object")

    def _test_invalid_outer_key_selectors(self):
        """
        Helper method to test if seemingly valid outer_key_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter outer_key_selector must have exactly one parameter
            for item in self._linq.group_join(self._inner_iterable,
                                               lambda person, index: person.name,
                                               self._valid_inner_key_selector,
                                               self._valid_result_selector):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter outer_key_selector must have exactly one parameter - and it cannot be keyword argument
            for item in self._linq.group_join(self._inner_iterable,
                                               lambda **kwargs: kwargs["item"].name,
                                               self._valid_inner_key_selector,
                                               self._valid_result_selector):
                item += 1

    def _test_invalid_inner_key_selector_parameter(self):
        """
        Helper method to test if invalid inner_key_selector parameters causes TypeError when group_join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter inner_key_selector must be a callable
            self._linq.group_join([], lambda x: x, 5, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter inner_key_selector cannot be None - it is not optional
            self._linq.group_join([], lambda x: x, None, lambda x: x)
        self.assertEqual(str(context.exception), "Parameter 'inner_key_selector' must be a 'callable' object")

    def _test_invalid_inner_key_selectors(self):
        """
        Helper method to test if seemingly valid inner_key_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter inner_key_selector must have exactly one parameter
            for item in self._linq.group_join(self._inner_iterable,
                                               self._valid_outer_key_selector,
                                               lambda person, index: person.name,
                                               self._valid_result_selector):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter inner_key_selector must have exactly one parameter - and it cannot be keyword argument
            for item in self._linq.group_join(self._inner_iterable,
                                               self._valid_outer_key_selector,
                                               lambda **kwargs: kwargs["item"].name,
                                               self._valid_result_selector):
                item += 1

    def _test_invalid_result_selector_parameter(self):
        """
        Helper method to test if invalid result_selector parameters causes TypeError when group_join() is called
        """
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.group_join([], lambda x: x, lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector cannot be None - it is not optional
            self._linq.group_join([], lambda x: x, lambda x: x, None)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    def _test_invalid_result_selectors(self):
        """
        Helper method to test if seemingly valid result_selector parameters causes TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # Parameter result_selector must have exactly two parameters
            for item in self._linq.group_join(self._inner_iterable,
                                               self._valid_outer_key_selector,
                                               self._valid_inner_key_selector,
                                               lambda x: x):
                item += 1
        with self.assertRaises(TypeError):
            # Parameter result_selector must have exactly two parameters - and they cannot be keyword arguments
            for item in self._linq.group_join(self._inner_iterable,
                                               self._valid_outer_key_selector,
                                               self._valid_inner_key_selector,
                                               lambda **kwargs: None):
                item += 1

    @staticmethod
    def _valid_result_selector(person: Person, houses: typing.List[House]) -> typing.Tuple[str, typing.List[int]]:
        return person.name, [house.address for house in houses]
