from nxsim import BaseNetworkAgent
from collections import OrderedDict
from copy import deepcopy
import json

from functools import wraps


class BaseBehaviour(BaseNetworkAgent):
    """
    A special simpy BaseNetworkAgent that keeps track of its state history.
    """

    def __init__(self, *args, **kwargs):
        self._history = OrderedDict()
        self._last_now = -1
        super().__init__(*args, **kwargs)

    @property
    def now(self):
        try:
            return self.env.now
        except AttributeError:
            # No environment
            return None

    @property
    def state(self):
        now = self.now
        if now and now != self._last_now:
            self._history[now] = self._state
            self._state = deepcopy(self._state)
            self._last_now = now
        return self._state

    @state.setter
    def state(self, value):
        self._state = value
        if self.now:
            self._history[self.now] = value

    def run(self):
        while True:
            self.step()
            timeout = self.env.environment_params.get("timeout", 1)
            yield self.env.timeout(timeout)

    def step(self):
        pass

    def to_json(self):
        return json.dumps(self._history)


def state(func):

    @wraps(func)
    def func_wrapper(self):
        next_state = func(self)
        if next_state:
            try:
                self.state['id'] = next_state.id
            except AttributeError:
                raise NotImplemented('State id %s is not valid.' % next_state)
        else:
            raise Exception('State {} returned no next state'.format(func))

    func_wrapper.id = func.__name__
    return func_wrapper


class MetaFSM(type):
    def __init__(cls, name, bases, nmspc):
        super(MetaFSM, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'states'):
            cls.states = {}
        # Re-use states from inherited classes
        for i in bases:
            if isinstance(i, MetaFSM):
                for state_id, state in i.states.items():
                    cls.states[state_id] = state

        # Add new states
        for name, func in nmspc.items():
            if hasattr(func, 'id'):
                cls.states[func.id] = func


class FSM(BaseBehaviour, metaclass=MetaFSM):

    def step(self):
        try:
            self.states[self.state['id']](self)
        except KeyError:
            raise Exception('{} is not a valid state id'.format(self.state['id']))
