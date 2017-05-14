from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import Person


class TestToDictionary(TestBase):
    def setUp(self):
        self._people = [Person("Name1", 11), Person("Name2", 22), Person("Name3", 33)]
        self._linq = Linq(self._people)

    def test_invalid_parameters(self):
        """
        Tests that calling to_dictionary() should raise a TypeError, in case parameters are not callable objects
        or do not have the right signature
        """
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector must be a callable
            self._linq.to_dictionary(5)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter key_selector cannot be None - it is not optional
            self._linq.to_dictionary(None)
        self.assertEqual(str(context.exception), "Parameter 'key_selector' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter result_selector must be a callable
            self._linq.to_dictionary(lambda x: x, 5)
        self.assertEqual(str(context.exception), "Parameter 'result_selector' must be a 'callable' object")
        with self.assertRaises(TypeError):
            # Parameter key_selector must have only one positional argument for the item
            self._linq.to_dictionary(lambda item, index: item)
        with self.assertRaises(TypeError):
            # Parameter result_selector must have only one positional argument for the item
            self._linq.to_dictionary(lambda item: item, lambda item, index: item)

    def test_valid_parameters(self):
        """
        Tests that calling to_dictionary() with a callable will not raise a TypeError
        """
        # Different types of callable objects
        self._linq.to_dictionary(lambda person: person.name)
        self._linq.to_dictionary(self._key_selector, None)
        self._linq.to_dictionary(self._key_selector, lambda person: person.age)
        self._linq.to_dictionary(self._key_selector, self._result_selector)

    def test_execution(self):
        """
        Tests that the returned dictionary is holding the right data
        """
        dictionary = self._linq.to_dictionary(self._key_selector)
        keys = set(dictionary.keys())
        values = set(dictionary.values())
        self.assertEqual(keys, {"Name1", "Name2", "Name3"})
        self.assertEqual(values, set(self._people))
        dictionary = self._linq.to_dictionary(self._key_selector, self._result_selector)
        keys = set(dictionary.keys())
        values = set(dictionary.values())
        self.assertEqual(keys, {"Name1", "Name2", "Name3"})
        self.assertEqual(values, {11, 22, 33})

    @staticmethod
    def _key_selector(person: Person):
        return person.name

    @staticmethod
    def _result_selector(person: Person):
        return person.age
