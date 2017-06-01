"""Runaway core."""


# [ Imports ]
# [ -Python ]
import sys
from collections import namedtuple
from functools import wraps
# [ -Project ]
from . import actions
from . import handlers as signal_handlers


# [ API ]
DEFAULT_HANDLERS = {
    'call': signal_handlers.handle_call,
    'sleep': signal_handlers.handle_sleep,
    'future': signal_handlers.handle_future,
    'waitfor': signal_handlers.handle_wait,
    'cancel': signal_handlers.handle_cancel,
}


def run(coro, **handlers):
    """Run the given coroutine."""
    if not handlers:
        handlers = DEFAULT_HANDLERS
    queue = []
    initial_action = actions.Send(coro, value=None, source=None)
    queue.append(initial_action)

    def _run_finalizer(async_generator):
        """Finalize the generator."""
        run(async_generator.aclose(), **handlers)

    old_hooks = sys.get_asyncgen_hooks()
    sys.set_asyncgen_hooks(finalizer=_run_finalizer)

    try:
        while True:
            action, *queue = queue
            outcome = _run_single(action)
            _log_state(action, queue, outcome)
            queue = _handle_outcome(outcome, handlers=handlers, action=action, queue=queue)
    except StopIteration as result:
        return result.value
    finally:
        sys.set_asyncgen_hooks(*old_hooks)


# [ Internal ]
def _log_state(action, queue, outcome):
    """Log the state."""
    if True:
        return
    message = f"\naction: {action}\nqueue:\n"
    for item in queue:
        message += f"\t{item}\n"
    message += f"outcome: {outcome}"
    print(message)


class Error:
    """An error result."""

    def __init__(self, data):
        """Init state."""
        self.data = data

    def __str__(self):
        """Get string representation."""
        return f"Error: {self.data}"


class ReturnValue:
    """A returned result."""

    def __init__(self, data):
        """Init state."""
        self.data = data

    def __str__(self):
        """Get string representation."""
        return f"ReturnValue: {self.data}"


ExcInfo = namedtuple('ExcInfo', 'exc_type exception traceback')


def try_catch_railway(func):
    """Decorator to convert exception-raising code to a railway switch."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper for try_catch_railway decorator."""
        try:
            return ReturnValue(func(*args, **kwargs))
        except:
            return Error(ExcInfo(*sys.exc_info()))

    return wrapper


@try_catch_railway
def _run_single(action):
    """Run a single action."""
    if isinstance(action, actions.Send):
        signal = _run_send(action)
    elif isinstance(action, actions.Throw):
        signal = _run_throw(action)
    elif isinstance(action, actions.Close):
        signal = _run_close(action)
    else:
        raise RuntimeError("Cannot execute non-action.")
    return signal


def _run_send(action):
    """Run a send action."""
    return action.coro.send(action.value)


def _run_throw(action):
    """Run a throw action."""
    return action.coro.throw(*action.exc_info)


def _run_close(action):
    """Run a close action."""
    return action.coro.close()


def _pass_error_to_source(exc_info, *, source, queue):
    """Pass an error up to the source."""
    # if a return value, send it back to the source
    if exc_info.exc_type == StopIteration:
        return queue + [actions.Send(source.coro, exc_info.exception.value, source.source)]
    # otherwise, raise it in the source
    return queue + [actions.Throw(source.coro, exc_info, source.source)]


def _handle_error(exc_info, *, action, queue):
    """Handle error."""
    # if there's a source, throw the exception up into them
    if action.source:
        return _pass_error_to_source(exc_info, source=action.source, queue=queue)
    # else, raise it directly.
    raise exc_info.exception.with_traceback(exc_info.traceback)


def _handle_signal(signal, *, handlers, action, queue):
    """Handle signal."""
    signal_type_name = type(signal).__name__.lower()
    try:
        return handlers[signal_type_name](signal, action=action, queue=queue)
    except KeyError:
        raise RuntimeError(f"No handler supplied for signal of type '{signal_type_name}'")


def _handle_outcome(outcome, *, handlers, action, queue):
    """Handle outcome."""
    if isinstance(outcome, Error):
        result = _handle_error(outcome.data, action=action, queue=queue)
    elif outcome.data is None:
        result = queue
    else:
        result = _handle_signal(outcome.data, handlers=handlers, action=action, queue=queue)
    return result
