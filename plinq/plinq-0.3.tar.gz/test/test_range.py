from test.test_base import TestBase
from plinq.linq import Linq


class TestRange(TestBase):
    def test_complex(self):
        iterable = [1, 2.0, 3.0, 4, 5.0, 6.0, 7, 8, 9]
        expected_values = [("2.0", 2.0), ("6.0", 6.0)]
        test_range = Linq(iterable).of_type(float)\
                                   .where(lambda item, index: item % 2 == 0)\
                                   .select(lambda item, index: str(item))\
                                   .reverse()\
                                   .order_by()\
                                   .concat([10, 20])\
                                   .zip([2.0, 6.0], lambda a, b: (a, b))
        self._test_range(test_range, expected_values)
