from test.test_base import TestBase
from test.utils import Person


class TestConcat(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling concat() should raise a TypeError, if iterable is not really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must be an iterable
            self._linq.concat(5)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable cannot be None - it is not optional
            self._linq.concat(None)
        self.assertEqual(str(context.exception), "Parameter 'iterable' must be an 'iterable' object")

    def test_valid_parameters(self):
        """
        Tests that calling concat() with an iterable will not raise a TypeError
        """
        # Different types of iterables
        self._linq.concat([])
        self._linq.concat({})
        self._linq.concat(set())
        self._linq.concat("")

    def test_iteration(self):
        """
        Tests that using concat with the right parameter, will not raise a TypeError when iteration starts
        Tests also, that concatenation takes effect
        """
        self._test_range(self._linq.concat([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5, 1, 2, 3, 4, 5])
        self._test_range(self._linq.concat([]), [1, 2, 3, 4, 5])
        self._test_range(self._linq.concat(["1", "2"]), [1, 2, 3, 4, 5, "1", "2"])
        self._test_range(self._linq.concat([Person("Name", 66, [12])]), [1, 2, 3, 4, 5, Person("Name", 66, [12])])
