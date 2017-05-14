from test.test_base import TestBase
from plinq.linq import Linq
from test.utils import test_iteration
from test.utils import NoneIteratorIterable
from test.utils import IntIteratorIterable
from test.utils import FakeIteratorIterable
from test.utils import ValidIteratorIterable


class TestRange(TestBase):
    def test__check_iterable(self):
        """
        Tests that _check_iterable raises TypeError when the provided parameter is not an iterable,
        and raises no error when the parameter looks like really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            self._linq._check_iterable(5, name="iterable1")
        self.assertEqual(str(context.exception), "Parameter 'iterable1' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            self._linq._check_iterable(NoneIteratorIterable(), name="iterable2")
        self.assertEqual(str(context.exception), "Parameter 'iterable2' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            self._linq._check_iterable(IntIteratorIterable(), name="iterable3")
        self.assertEqual(str(context.exception), "Parameter 'iterable3' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            self._linq._check_iterable(FakeIteratorIterable(), name="iterable4")
        self.assertEqual(str(context.exception), "Parameter 'iterable4' must be an 'iterable' object")
        # If everything is OK, _check_iterable should not raise any error
        self._linq._check_iterable([], name="iterable")
        self._linq._check_iterable({}, name="iterable")
        self._linq._check_iterable(set(), name="iterable")
        self._linq._check_iterable(ValidIteratorIterable(), name="iterable")

    def test__check_callable(self):
        with self.assertRaises(TypeError) as context:
            # Parameter callable must be a callable
            self._linq._check_callable(5, name="callable1")
        self.assertEqual(str(context.exception), "Parameter 'callable1' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter callable must be a callable or None if it is optional
            self._linq._check_callable(5, name="callable2", optional=True)
        self.assertEqual(str(context.exception), "Parameter 'callable2' must be a 'callable' object")
        # If the parameter is a callable everything should be ok  even if the parameter is optional
        self._linq._check_callable(lambda x: x, name="callable")
        self._linq._check_callable(self._callable, name="callable")

        def f():
            pass

        self._linq._check_callable(f, name="callable")
        self._linq._check_callable(lambda x: x, name="callable", optional=True)
        # If the parameter is optional it can also be None
        self._linq._check_callable(None, name="callable", optional=True)

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
        try:
            test_iteration(test_range, expected_values)
        except AssertionError as error:
            self.assertTrue(False, str(error))

    def _callable(self):
        pass
