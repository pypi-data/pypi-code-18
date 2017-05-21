from plinq.utils import check_callable
from plinq.utils import check_iterable
from test.test_base import TestBase
from test.utils import NoneIteratorIterable
from test.utils import IntIteratorIterable
from test.utils import FakeIteratorIterable
from test.utils import ValidIteratorIterable


class TestUtils(TestBase):
    def test_check_iterable(self):
        """
        Tests that check_iterable raises TypeError when the provided parameter is not an iterable,
        and raises no error when the parameter looks like really an iterable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            check_iterable(5, name="iterable1")
        self.assertEqual(str(context.exception), "Parameter 'iterable1' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            check_iterable(NoneIteratorIterable(), name="iterable2")
        self.assertEqual(str(context.exception), "Parameter 'iterable2' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            check_iterable(IntIteratorIterable(), name="iterable3")
        self.assertEqual(str(context.exception), "Parameter 'iterable3' must be an 'iterable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter iterable must produce an object which looks like an iterator
            check_iterable(FakeIteratorIterable(), name="iterable4")
        self.assertEqual(str(context.exception), "Parameter 'iterable4' must be an 'iterable' object")
        # If everything is OK, check_iterable should not raise any error
        check_iterable([], name="iterable")
        check_iterable({}, name="iterable")
        check_iterable(set(), name="iterable")
        check_iterable(ValidIteratorIterable(), name="iterable")

    def test_check_callable(self):
        """
        Tests that check_callable raises TypeError when the provided parameter is not a callable,
        and raises no error when the parameter looks like really a callable
        """
        with self.assertRaises(TypeError) as context:
            # Parameter callable must be a callable
            check_callable(5, name="callable1")
        self.assertEqual(str(context.exception), "Parameter 'callable1' must be a 'callable' object")
        with self.assertRaises(TypeError) as context:
            # Parameter callable must be a callable or None if it is optional
            check_callable(5, name="callable2", optional=True)
        self.assertEqual(str(context.exception), "Parameter 'callable2' must be a 'callable' object")
        # If the parameter is a callable everything should be ok  even if the parameter is optional
        check_callable(lambda x: x, name="callable")
        check_callable(self._callable, name="callable")

        def f():
            pass
        check_callable(f, name="callable")
        check_callable(lambda x: x, name="callable", optional=True)
        # If the parameter is optional it can also be None
        check_callable(None, name="callable", optional=True)

    def _callable(self):
        pass
