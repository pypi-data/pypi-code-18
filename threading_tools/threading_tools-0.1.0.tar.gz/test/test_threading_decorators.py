import unittest
import threading
from threading_tools import SynchronizedNumber
from threading_tools import threaded_fn


class TestThreadingDecorators(unittest.TestCase):

    def test_threaded_fn(self):
        main_thread = threading.current_thread()

        @threaded_fn
        def function_to_thread(main_thread, arg0, arg1, kwarg0=5, kwarg1=5):
            result = arg0 + arg1 + kwarg0 + kwarg1
            assert result == 26, \
                'Sum of numerical args should be 26. Instead it was {0}'.format(result)
            assert main_thread != threading.current_thread(), \
                'Inside function_to_thread main_thread should NOT be the current thread'

        function_to_thread(main_thread, 5, 6, kwarg0=7, kwarg1=8)
        assert main_thread == threading.current_thread(), \
            'Outside function_to_thread, main_thread should be the current thread'
