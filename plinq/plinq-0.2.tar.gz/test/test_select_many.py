from test.test_base import TestBase
from test.utils import Person
from plinq.linq import Linq


class TestSelectMany(TestBase):
    def setUp(self):
        people = [Person("Name1", 11, [11, 12]), Person("Name2", 22, [21, 22, 23]), Person("Name3", 33, [31])]
        self._linq = Linq(people)

    def test_invalid_parameters(self):
        """
        Tests that calling select_many() should raise a TypeError, in case parameters are not callable objects
        """
        self._test_invalid_collection_selector_parameter()
        self._test_invalid_result_selector_parameter()

    def test_valid_parameters(self):
        """
        Tests that calling select_many() with a callable will not raise a TypeError
        """
        # Different types of callable objects as selectors
        self._linq.select_many(lambda item, index: item)
        self._linq.select_many(self._collection_selector_with_parameters, lambda x, y: (x, y))

    def test_iteration_with_wrong_selectors(self):
        """
        Tests that using select_many with wrong selectors will raise a TypeError when iteration starts
        """
        with self.assertRaises(TypeError):
            # collection_selector must have two parameters
            for item in self._linq.select_many(lambda x: True):
                item += 1
        with self.assertRaises(TypeError):
            # result selector must have two parameters too
            for item in self._linq.select_many(lambda i, index: i, lambda x, y, z: True):
                item += 1

    def test_iteration_with_right_selectors(self):
        """
        Tests that using select_many with the right selectors, will not raise a TypeError when iteration starts
        Tests also, that predicate takes effect
        """
        expected_values = [11, 12, 21, 22, 23, 31]
        self._test_range(self._linq.select_many(self._collection_selector_with_parameters), expected_values)
        expected_values = [11.0, 12.0, 21.0, 22.0, 23.0, 31.0]
        self._test_range(self._linq.select_many(self._collection_selector_with_parameters,
                                                 lambda item, collection_item: float(collection_item)),
                         expected_values)

    def test_lazy_execution(self):
        """
        Tests that selector will not be invoked until iterating takes place
        """
        collection_selector_counter = 0
        result_selector_counter = 0

        def collection_selector(item: Person, index):
            nonlocal collection_selector_counter
            collection_selector_counter += 1
            index += 1
            return item.phone_numbers

        def result_selector(person, phone_number):
            nonlocal result_selector_counter
            result_selector_counter += 1
            return person.name, phone_number
        select_many_range = self._linq.select_many(collection_selector, result_selector)
        self.assertEqual(collection_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        select_many_iterator = iter(select_many_range)
        self.assertEqual(collection_selector_counter, 0)
        self.assertEqual(result_selector_counter, 0)
        self.assertEqual(("Name1", 11), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 1)
        self.assertEqual(result_selector_counter, 1)
        self.assertEqual(("Name1", 12), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 1)
        self.assertEqual(result_selector_counter, 2)
        self.assertEqual(("Name2", 21), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 2)
        self.assertEqual(result_selector_counter, 3)
        self.assertEqual(("Name2", 22), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 2)
        self.assertEqual(result_selector_counter, 4)
        self.assertEqual(("Name2", 23), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 2)
        self.assertEqual(result_selector_counter, 5)
        self.assertEqual(("Name3", 31), next(select_many_iterator))
        self.assertEqual(collection_selector_counter, 3)
        self.assertEqual(result_selector_counter, 6)

    def _test_invalid_collection_selector_parameter(self):
        with self.assertRaises(TypeError) as context:
            # Parameter collection_selector must be a callable
            self._linq.select_many(5)
        self.assertEqual(str(context.exception), "Parameter 'collection_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter collection_selector cannot be None - it is not optional
            self._linq.select_many(None)
        self.assertEqual(str(context.exception), "Parameter 'collection_selector' must be a 'callable' object")

    def _test_invalid_result_selector_parameter(self):
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.select_many(lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")

    @staticmethod
    def _collection_selector_with_parameters(item: Person, index: int):
        index += 1
        return item.phone_numbers
