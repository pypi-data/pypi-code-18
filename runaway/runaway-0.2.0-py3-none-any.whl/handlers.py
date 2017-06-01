"""Runaway signal handlers."""


# [ Imports ]
# [ -Python ]
import time
from collections import namedtuple
import pprint
# [ -Third Party ]
import utaw
# [ -Project ]
from . import actions
from . import signals


# [ API ]
def handle_call(call_signal, *, action, queue):
    """Handle a call."""
    async def wrapping_coro():
        """A wrapping coro for a call."""
        value_or_coro = call_signal.func(*call_signal.args, **call_signal.kwargs)
        # EARLY RETURN
        if _is_coro(value_or_coro):
            coro = value_or_coro
            return await coro
        value = value_or_coro
        return value

    return queue + [actions.Send(wrapping_coro(), value=None, source=action)]


class WakeupCoroProxy:
    """A coro proxy for wakeups."""

    def __init__(self, coro, *, wake_time):
        """Init the state."""
        self._coro = coro
        self.wake_time = wake_time

    def send(self, value):
        """Send value to coro."""
        return self._coro.send(value)

    def throw(self, exc_info):
        """Throw exc info into coro."""
        return self._coro.throw(exc_info)

    def close(self):
        """Close coro."""
        return self._coro.close()


def _all_sleep_actions(queue):
    """Return whether all the things in the queue are sleep actions."""
    return (
        all(isinstance(i, actions.Send) for i in queue) and
        all(isinstance(i.coro, WakeupCoroProxy) for i in queue)
    )


def _sort_sleep_actions(queue):
    """Return sorted sleep actions."""
    return sorted(queue, key=lambda i: i.coro.wake_time)


def handle_sleep(sleep_signal, *, action, queue, sleep=time.sleep, now=time.time):
    """Handle a sleep signal."""
    # first, determine sleep end time
    wake_time = now() + sleep_signal.seconds

    # next, schedule checkup.
    async def wakeup_coro():
        """A wakeup coro for the sleep signal."""
        while now() < wake_time:
            await signals.sleep(0)

    coro = WakeupCoroProxy(wakeup_coro(), wake_time=wake_time)
    new_queue = queue + [actions.Send(coro, value=None, source=action)]

    # EARLY EXIT
    if not _all_sleep_actions(new_queue):
        return new_queue

    sorted_sleep_actions = _sort_sleep_actions(new_queue)
    soonest_wake = sorted_sleep_actions[0].coro.wake_time
    time_to_sleep = max(0, soonest_wake - now())
    sleep(time_to_sleep)
    return sorted_sleep_actions



def test_handle_multi_sleep():
    """Test."""
    # Given
    sleep_signal = signals.Sleep(7)
    action = actions.Send(None, value=None, source=None)  # action doesn't matter
    queue = [
        actions.Send(WakeupCoroProxy(None, wake_time=10), value=None, source=None),
        actions.Send(WakeupCoroProxy(None, wake_time=5), value=None, source=None),
        actions.Send(WakeupCoroProxy(None, wake_time=1), value=None, source=None),
        actions.Send(WakeupCoroProxy(None, wake_time=20), value=None, source=None),
    ]

    sleep_time = None

    def fake_sleep(seconds):
        """Record sleep time."""
        nonlocal sleep_time

        sleep_time = seconds

    expected_sleep_time = 1
    expected_wake_times = [1, 5, 7, 10, 20]

    def fake_now():
        """Return fake now time."""
        return 0

    # When
    queue = handle_sleep(sleep_signal, action=action, queue=queue, sleep=fake_sleep, now=fake_now)

    # Then
    wake_times = [a.coro.wake_time for a in queue]
    utaw.assertEqual(expected_sleep_time, sleep_time)
    utaw.assertListEqual(expected_wake_times, wake_times)

    # kill the actual coro that was created
    queue[2].coro.close()


class Future:
    """The future class."""
    NOT_DONE = object()

    def __init__(self, func, *args, **kwargs):
        """Init the state."""
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = self.NOT_DONE
        self._exc_info = None
        self._cancelled = False

    @property
    def done(self):
        """Return whether the future is done or not."""
        return self.cancelled or self.result is not self.NOT_DONE or self.exception is not None

    def set_cancelled(self):
        """Mark the future as cancelled from the cancel handler."""
        self._cancelled = True

    # TODO - need better cancellation semantics - some way to express
    # an expectation that the future was/was-not done?
    # cancel/ensure_cancelled/ensure_done?
    @property
    def cancelled(self):
        """Return whether or not the coro is cancelled."""
        return self._cancelled

    @property
    def exception(self):
        """Return the exception, if any, else None."""
        return self._exc_info

    def set_exception(self, exc_info):
        """Set the exception."""
        self._exc_info = exc_info

    # def __eq__(self, other):
    #     """Return whether self is equal to other."""
    #     return (
    #         isinstance(other, type(self)) and
    #         self.__dict__ == other.__dict__
    #     )

    def __str__(self):
        """String representation."""
        return pprint.pformat((type(self), self.__dict__))

    __repr__ = __str__


def _from_future(action, *, future):
    """Return the coros from the action that are children of the future."""
    coros = []
    future_matched = False
    while action.source:
        coros.append(action.coro)
        if getattr(action.source, 'future', None) is future:
            future_matched = True
            break
        action = action.source
    if not future_matched:
        return []
    else:
        return coros


def handle_cancel(cancel_signal, *, action, queue):
    """Handle a cancel signal."""
    the_future = cancel_signal.future

    new_queue = []
    to_close = []
    for this_action in queue:
        child_coros = _from_future(this_action, future=the_future)
        if child_coros:
            to_close += child_coros
        else:
            new_queue.append(this_action)
    to_close = set(to_close)
    close_actions = [actions.Close(c, source=action.source) for c in to_close]
    the_future.set_cancelled()
    return close_actions + new_queue + [actions.Send(action.coro, value=None, source=action.source)]


def handle_future(future_signal, *, action, queue):
    """Handle a future signal."""
    # create a future.
    the_future = Future(future_signal.func, *future_signal.args, **future_signal.kwargs)

    # init the actions list
    new_actions = []

    # send the future back to the caller
    new_actions.append(actions.Send(action.coro, value=the_future, source=action.source))

    # also run the future
    async def future_coro():
        """A wrapping coro for a future."""
        value_or_coro = future_signal.func(*future_signal.args, **future_signal.kwargs)

        # EARLY RETURN
        if _is_coro(value_or_coro):
            coro = value_or_coro
            return await coro
        value = value_or_coro
        return value

    action_proxy = FutureActionProxy(the_future)
    new_actions.append(actions.Send(future_coro(), value=None, source=action_proxy))

    return queue + new_actions


WaitResult = namedtuple('WaitResult', 'completed remaining timed_out')


def handle_wait(wait_signal, *, action, queue, now=time.time):
    """Handle the wait signal."""
    end_time = None if wait_signal.timeout is None else now() + wait_signal.timeout

    # schedule waiter.
    async def waiting_coro():
        """A waiting coro for the wait signal."""
        def timed_out():
            """Return whether or not the wait timed out."""
            # EARLY RETURN
            if end_time is None:
                return False
            return end_time < now()

        def should_wait():
            """Return whether or not to wait."""
            done_futures = [f for f in wait_signal.futures if f.done]
            return (len(done_futures) < wait_signal.minimum_done) and not timed_out()

        while should_wait():
            await signals.sleep(0)

        done = []
        remaining = []
        for future in wait_signal.futures:
            if future.done:
                done.append(future)
            else:
                remaining.append(future)

        if wait_signal.cancel_remaining:
            for this_future in remaining:
                await signals.cancel(this_future)

        return WaitResult(done, remaining, timed_out())

    return queue + [actions.Send(waiting_coro(), value=None, source=action)]


# [ Internals ]
class FutureActionProxy:
    """
    A proxy for future actions.

    When someone tries to throw or send a value to the source of a future action,
    it should get shunted to the future's data, not back to the actual source.
    """

    def __init__(self, the_future):
        """Init the state."""
        self.coro = FutureCoroSourceProxy(the_future)
        self.source = None
        self.future = the_future


class FutureCoroSourceProxy:
    """
    A proxy for future source actions.

    When someone tries to throw or send a value to the source of a future action,
    it should get shunted to the future's data, not back to the actual source.
    """

    def __init__(self, the_future):
        """Init the state."""
        self._future = the_future

    def send(self, value):
        """
        Send the value to the future source.

        Typically used to send the return value from a coroutine call in as the
        result of that call.
        """
        self._future.result = value
        return None

    def throw(self, *exc_info):
        """
        Throw the exception info to the future source.

        Typically used to raise an exception from the future's target function.
        """
        self._future.set_exception(exc_info)
        return None


def _is_coro(maybe_coro):
    """Return whether or not the thing is a coro."""
    try:
        return (
            maybe_coro.send and
            maybe_coro.throw and
            maybe_coro.close
        )
    except AttributeError:
        return False
