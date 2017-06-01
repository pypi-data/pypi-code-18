"""
Helpers for looping.

The functions defined here are functional loops, which you can
use to both perform async loops and assist in testing.

We've tested these functions so you don't have to.  All you have to do
is test your iteration funcs, predicate funcs, and that you're calling
these loop funcs, and you can gain some confidence in your looping code.
"""


# [ Imports ]
# [ -Third Party ]
import utaw
# [ -Project ]
from runaway.signals import call, Call
from runaway.testing import TestWrapper, assertEqual


# [ API ]
async def do_while(predicate, iteration_func, state):
    """
    Do iteration func and continue to do it while the predicate is true.

    Passes state to iteration_func on the first run.

    On each subsequent run, the result from iteration_func is used as
    the state.

    The state is passed into the predicate, and if that evaluates:
        * true: the state is passed into the iteration_func to start another cycle
        * false: the state is returned to the caller as returned from the iteration_func
    """
    iteration_result = await call(iteration_func, state)
    while await call(predicate, iteration_result):
        iteration_result = await call(iteration_func, iteration_result)
    return iteration_result


async def run_forever(iteration_func, state):
    await call(do_while, _return_true, iteration_func, state)


# [ Internal ]
def _return_true(_):
    return True


# [ Tests ]
class DoWhile:

    def __init__(self, predicate, iteration_func, state):
        self._predicate = predicate
        self._iteration_func = iteration_func
        self._state = state
        self._coro = TestWrapper(
            do_while(
                self._predicate,
                self._iteration_func,
                self._state,
            )
        )
        self._result = None

    def runs_iteration_and_gets_1(self):
        assertEqual(self._coro.signal, Call(self._iteration_func, self._state))
        self._result = 1
        self._coro.receives_value(self._result)

    def runs_predicate_and_gets_false(self):
        assertEqual(self._coro.signal, Call(self._predicate, self._result))
        self._coro.receives_value(False)

    def runs_predicate_and_gets_true(self):
        assertEqual(self._coro.signal, Call(self._predicate, self._result))
        self._coro.receives_value(True)

    def returns_1(self):
        assertEqual(self._coro.returned, self._result)

def test_run_forever():
    iteration_func = object()
    state = object()
    coro = TestWrapper(run_forever(iteration_func, state))

    assertEqual(coro.signal, Call(do_while, _return_true, iteration_func, state))


def test_do_while_done_after_1():

    def predicate(value):
        return NotImplementedError

    def iteration(prev_value):
        return NotImplementedError

    target = DoWhile(predicate, iteration, 0)
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_false()
    target.returns_1()


def test_do_while_done_after_5():

    def predicate(value):
        return NotImplementedError

    def iteration(prev_value):
        return NotImplementedError

    target = DoWhile(predicate, iteration, 1)
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_true()
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_true()
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_true()
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_true()
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_true()
    target.runs_iteration_and_gets_1()
    target.runs_predicate_and_gets_false()
    target.returns_1()


def test_return_true():
    utaw.assertIs(True, _return_true(None))


