"""Runaway built-in signals."""


# [ Imports ]
import types
import pprint


# [ Signals ]
class Call:
    """Call a function."""

    def __init__(self, func, *args, **kwargs):
        """Init the state."""
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.func == other.func and
            self.args == other.args and
            self.kwargs == other.kwargs
        )

    def __str__(self):
        """String representation."""
        return pprint.pformat((type(self), self.__dict__))

    __repr__ = __str__


class Sleep:
    """Sleep for n seconds."""

    def __init__(self, seconds):
        """Init the state."""
        self.seconds = seconds

    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.__dict__ == other.__dict__
        )

    def __str__(self):
        """String representation."""
        return pprint.pformat((type(self), self.__dict__))

    __repr__ = __str__

class Future:
    """Create a future for a function call."""

    def __init__(self, func, *args, **kwargs):
        """Init the state."""
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.func == other.func and
            self.args == other.args and
            self.kwargs == other.kwargs
        )

    def __str__(self):
        """String representation."""
        return pprint.pformat((type(self), self.__dict__))

    __repr__ = __str__
    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.func == other.func and
            self.args == other.args and
            self.kwargs == other.kwargs
        )

    def __str__(self):
        """String representation."""
        return pprint.pformat((type(self), self.__dict__))

    __repr__ = __str__


class WaitFor:
    """Wait for futures."""
    def __init__(self, *futures, minimum_done, cancel_remaining, timeout):
        """Init the state."""
        self.futures = set(futures)
        self.minimum_done = minimum_done
        self.cancel_remaining = cancel_remaining
        self.timeout = timeout

    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.__dict__ == other.__dict__
        )

    def __str__(self):
        """String representation."""
        return str(self.__dict__)

    def __repr__(self):
        """Representation of object."""
        return str(self)


class Cancel:
    """Cancel a future."""
    def __init__(self, future):
        """Init the state."""
        self.future = future

    def __eq__(self, other):
        """Return whether self is equal to other."""
        return (
            isinstance(other, type(self)) and
            self.__dict__ == other.__dict__
        )

    def __str__(self):
        """String representation."""
        return str(self.__dict__)

    def __repr__(self):
        """Representation of object."""
        return str(self)


# [ Signal Creators ]
@types.coroutine
def call(func, *args, **kwargs):
    """Create a signal from the given args."""
    return (yield Call(func, *args, **kwargs))


@types.coroutine
def sleep(seconds):
    """Create a signal from the given args."""
    return (yield Sleep(seconds))


@types.coroutine
def future(func, *args, **kwargs):
    """Create a signal from the given args."""
    return (yield Future(func, *args, **kwargs))


@types.coroutine
def wait_for(*futures, minimum_done=None, cancel_remaining=True, timeout=None):
    """Create a signal from the given args."""
    if minimum_done is None:
        minimum_done = len(futures)
    elif len(futures) < minimum_done:
        raise ValueError(f"Cannot wait for minimum_done of {minimum_done} with only {len(futures)} futures supplied.")
    return (yield WaitFor(*futures, minimum_done=minimum_done, cancel_remaining=cancel_remaining, timeout=timeout))


@types.coroutine
def cancel(future):
    """Create a signal from the given args."""
    return (yield Cancel(future))
