import typing
from unittest import TestCase
from plinq.linq import Linq


class TestBase(TestCase):
    def setUp(self):
        self._linq = Linq([1, 2, 3, 4, 5])

    def _test_range(self, test_range: Linq, expected_values: typing.List) -> None:
        counter = 0
        for item, expected_value in zip(test_range, expected_values):
            self.assertEqual(item, expected_value)
            counter += 1
        self.assertEqual(counter, len(expected_values))

    def _test_set(self, test_range: Linq, expected_values: typing.Set) -> None:
        test_set = set(test_range)
        self.assertEqual(test_set, expected_values)
