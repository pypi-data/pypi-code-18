import unittest
import threading
from threading_tools import SynchronizedNumber, LockAcquisitionException

NUM_TRIALS = 2500


class TestSynchronizedNumber(unittest.TestCase):

    def test_increment(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(0.0)

            thread1_incr_amt = 50
            thread2_incr_amt = 100

            thread1 = threading.Thread(target=sync_num.increment, args=(thread1_incr_amt, ))
            thread2 = threading.Thread(target=sync_num.increment, args=(thread2_incr_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 150, 'Trial {0}: sync_num is {1} but must be 150'.format(i, sync_num)

    def test_decrement(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(150.0)

            thread1_decr_amt = 50
            thread2_decr_amt = 100

            thread1 = threading.Thread(target=sync_num.decrement, args=(thread1_decr_amt, ))
            thread2 = threading.Thread(target=sync_num.decrement, args=(thread2_decr_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 0, 'Trial {0}: sync_num is {1} but must be 0'.format(i, sync_num)

    def test_strict_increment_if_less_than(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(0.0)

            thread1_incr_amt = 100
            thread2_incr_amt = 100
            limit = 100

            thread1 = threading.Thread(
                target=sync_num.increment_if_less_than, args=(thread1_incr_amt, limit))
            thread2 = threading.Thread(
                target=sync_num.increment_if_less_than, args=(thread2_incr_amt, limit))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 100, 'Trial {0}: sync_num is {1} but must be 100'.format(i, sync_num)

    def test_eq_ok_increment_if_less_than(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(0.0)

            thread1_incr_amt = 100
            thread2_incr_amt = 100
            limit = 100

            thread1 = threading.Thread(
                target=sync_num.increment_if_less_than, args=(thread1_incr_amt, limit, True))
            thread2 = threading.Thread(
                target=sync_num.increment_if_less_than, args=(thread2_incr_amt, limit, True))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 200, 'Trial {0}: sync_num is {1} but must be 200'.format(i, sync_num)

    def test_strict_decrement_if_greater_than(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(200.0)

            thread1_decr_amt = 100
            thread2_decr_amt = 100
            limit = 100

            thread1 = threading.Thread(
                target=sync_num.decrement_if_greater_than, args=(thread1_decr_amt, limit))
            thread2 = threading.Thread(
                target=sync_num.decrement_if_greater_than, args=(thread2_decr_amt, limit))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 100, 'Trial {0}: sync_num is {1} but must be 100'.format(i, sync_num)

    def test_eq_ok_decrement_if_greater_than(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(200.0)

            thread1_decr_amt = 100
            thread2_decr_amt = 100
            limit = 100

            thread1 = threading.Thread(
                target=sync_num.decrement_if_greater_than, args=(thread1_decr_amt, limit, True))
            thread2 = threading.Thread(
                target=sync_num.decrement_if_greater_than, args=(thread2_decr_amt, limit, True))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 0, 'Trial {0}: sync_num is {1} but must be 0'.format(i, sync_num)

    def test_increment_if_satisfies_condition(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(51.0)

            thread1_incr_amt = 40
            thread2_incr_amt = 40
            thread3_incr_amt = 40

            def condition(x):
                return 50 < x < 100

            thread1 = threading.Thread(
                target=sync_num.increment_if_satisfies_condition,
                args=(thread1_incr_amt, condition))
            thread2 = threading.Thread(
                target=sync_num.increment_if_satisfies_condition,
                args=(thread2_incr_amt, condition))
            thread3 = threading.Thread(
                target=sync_num.increment_if_satisfies_condition,
                args=(thread3_incr_amt, condition))

            # Start the threads
            thread1.start()
            thread2.start()
            thread3.start()

            # Wait on the threads
            thread1.join()
            thread2.join()
            thread3.join()

            assert sync_num == 131, 'Trial {0}: sync_num is {1} but must be 131'.format(i, sync_num)

    def test_decrement_if_satisfies_condition(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(99.0)

            thread1_decr_amt = 40
            thread2_decr_amt = 40
            thread3_decr_amt = 40

            def condition(x):
                return 50 < x < 100

            thread1 = threading.Thread(
                target=sync_num.decrement_if_satisfies_condition,
                args=(thread1_decr_amt, condition))
            thread2 = threading.Thread(
                target=sync_num.decrement_if_satisfies_condition,
                args=(thread2_decr_amt, condition))
            thread3 = threading.Thread(
                target=sync_num.decrement_if_satisfies_condition,
                args=(thread3_decr_amt, condition))

            # Start the threads
            thread1.start()
            thread2.start()
            thread3.start()

            # Wait on the threads
            thread1.join()
            thread2.join()
            thread3.join()

            assert sync_num == 19, 'Trial {0}: sync_num is {1} but must be 19'.format(i, sync_num)

    def test_lock_release_on_error(self):

        def condition(x):
            """
            This is an intentionally bad condition that triggers an error
            """
            return 'string' + x

        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(99.0)

            def wrapper_fn():
                try:
                    sync_num.decrement_if_satisfies_condition(40, condition)
                except Exception as e:
                    assert isinstance(e, TypeError), \
                        'The exception should be a TypeError. Instead was a {0}. {1}'.format(
                        type(e), e)

            thread1 = threading.Thread(target=wrapper_fn)
            thread1.start()
            thread1.join()

            assert not sync_num._lock.locked(), 'Trial {0}: The lock should not be locked. It was.'

    def test_set_value(self):
        """
        Note: this is a cursory functionality check. This does NOT test threadsafety.
        """
        sync_num = SynchronizedNumber(0.0)

        thread1_amt = 100
        thread1 = threading.Thread(target=sync_num.set_value, args=(thread1_amt, ))

        # Start the thread
        thread1.start()

        # Wait on the thread
        thread1.join()

        assert sync_num == 100, 'sync_num is {0} but must be 100'.format(sync_num)

    def test_iadd_success(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(0.0)

            thread1_incr_amt = 50
            thread2_incr_amt = 100

            def incr_wrapper(sync_num, amt):
                sync_num += amt

            thread1 = threading.Thread(target=incr_wrapper, args=(sync_num, thread1_incr_amt, ))
            thread2 = threading.Thread(target=incr_wrapper, args=(sync_num, thread2_incr_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 150, 'Trial {0}: sync_num is {1} but must be 150'.format(i, sync_num)

    def test_isub_success(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(150.0)

            thread1_decr_amt = 50
            thread2_decr_amt = 100

            def decr_wrapper(sync_num, amt):
                sync_num -= amt

            thread1 = threading.Thread(target=decr_wrapper, args=(sync_num, thread1_decr_amt, ))
            thread2 = threading.Thread(target=decr_wrapper, args=(sync_num, thread2_decr_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 0, 'Trial {0}: sync_num is {1} but must be 0'.format(i, sync_num)

    def test_imul_success(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(1.0)

            thread1_mul_amt = 5
            thread2_mul_amt = 10

            def mul_wrapper(sync_num, amt):
                sync_num *= amt

            thread1 = threading.Thread(target=mul_wrapper, args=(sync_num, thread1_mul_amt, ))
            thread2 = threading.Thread(target=mul_wrapper, args=(sync_num, thread2_mul_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert sync_num == 50, 'Trial {0}: sync_num is {1} but must be 50'.format(i, sync_num)

    def test_idiv_success(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(50.0)

            thread1_div_amt = 7
            thread2_div_amt = 10

            def div_wrapper(sync_num, amt):
                sync_num /= amt

            thread1 = threading.Thread(target=div_wrapper, args=(sync_num, thread1_div_amt, ))
            thread2 = threading.Thread(target=div_wrapper, args=(sync_num, thread2_div_amt, ))

            # Start the threads
            thread1.start()
            thread2.start()

            # Wait on the threads
            thread1.join()
            thread2.join()

            assert round(sync_num.value, 4) == 0.7143, \
                'Trial {0}: sync_num is {1} but must be 0.7143'.format(i, sync_num)

    def test_idivide_if_satisfies_condition(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(99.0)

            thread1_idiv_amt = 1.5
            thread2_idiv_amt = 1.5
            thread3_idiv_amt = 1.5

            def condition(x):
                return 50 < x < 100

            thread1 = threading.Thread(
                target=sync_num.idivide_if_satisfies_condition,
                args=(thread1_idiv_amt, condition))
            thread2 = threading.Thread(
                target=sync_num.idivide_if_satisfies_condition,
                args=(thread2_idiv_amt, condition))
            thread3 = threading.Thread(
                target=sync_num.idivide_if_satisfies_condition,
                args=(thread3_idiv_amt, condition))

            # Start the threads
            thread1.start()
            thread2.start()
            thread3.start()

            # Wait on the threads
            thread1.join()
            thread2.join()
            thread3.join()

            assert sync_num == 44, \
                'Trial {0}: sync_num is {1} but must be 44'.format(i, sync_num)

    def test_imultiply_if_satisfies_condition(self):
        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(51.0)

            thread1_imul_amt = 1.5
            thread2_imul_amt = 1.5
            thread3_imul_amt = 1.5

            def condition(x):
                return 50 < x < 100

            thread1 = threading.Thread(
                target=sync_num.imultiply_if_satisfies_condition,
                args=(thread1_imul_amt, condition))
            thread2 = threading.Thread(
                target=sync_num.imultiply_if_satisfies_condition,
                args=(thread2_imul_amt, condition))
            thread3 = threading.Thread(
                target=sync_num.imultiply_if_satisfies_condition,
                args=(thread3_imul_amt, condition))

            # Start the threads
            thread1.start()
            thread2.start()
            thread3.start()

            # Wait on the threads
            thread1.join()
            thread2.join()
            thread3.join()

            assert sync_num == 114.75, \
                'Trial {0}: sync_num is {1} but must be 114.75'.format(i, sync_num)

    def test_non_blocking_iadd(self):

        def iadd_wrapper(sync_num):
            try:
                sync_num += 5.0
                assert False, 'Exception was not thrown, but it should have been thrown'
            except Exception as e:
                assert isinstance(e, LockAcquisitionException), \
                    'The exception should be a LockAcquisitionException. Instead was a {0}. {1}' \
                    .format(type(e), e)

        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(10.0, should_block_thread=False)

            sync_num._lock.acquire()  # Acquire lock on main thread so others can't acquire it
            thread = threading.Thread(target=iadd_wrapper, args=(sync_num, ))
            thread.start()

            thread.join()
            sync_num._lock.release()

    def test_non_blocking_imul(self):

        def imul_wrapper(sync_num):
            try:
                sync_num *= 5.0
                assert False, 'Exception was not thrown, but it should have been thrown'
            except Exception as e:
                assert isinstance(e, LockAcquisitionException), \
                    'The exception should be a LockAcquisitionException. Instead was a {0}. {1}' \
                    .format(type(e), e)

        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(10.0, should_block_thread=False)

            sync_num._lock.acquire()  # Acquire lock on main thread so others can't acquire it
            thread = threading.Thread(target=imul_wrapper, args=(sync_num, ))
            thread.start()

            thread.join()
            sync_num._lock.release()

    def test_non_blocking_idiv(self):

        def idiv_wrapper(sync_num):
            try:
                sync_num /= 5.0
                assert False, 'Exception was not thrown, but it should have been thrown'
            except Exception as e:
                assert isinstance(e, LockAcquisitionException), \
                    'The exception should be a LockAcquisitionException. Instead was a {0}. {1}' \
                    .format(type(e), e)

        for i in range(NUM_TRIALS):
            sync_num = SynchronizedNumber(10.0, should_block_thread=False)

            sync_num._lock.acquire()  # Acquire lock on main thread so others can't acquire it
            thread = threading.Thread(target=idiv_wrapper, args=(sync_num, ))
            thread.start()

            thread.join()
            sync_num._lock.release()
