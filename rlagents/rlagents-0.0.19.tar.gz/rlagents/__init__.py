import random
from .tools import benchmark, gymwrapper
from .mc import MCAgent
from .ql import QLAgent

__version__ = (0, 0, 19)
__all__ = ['benchmark', '__version__', 'RandomAgent', 'gymwrapper',
           'MCAgent', 'QLAgent'
           ]


class RandomAgent:
    def __init__(self, actions):
        self.actions = actions
        self.reset()

    def reset(self):
        pass

    def copy(self):
        d = RandomAgent(self.actions)
        return d

    def get_action(self, observation):
        return random.choice(self.actions)

    def start_episode(self):
        pass

    def end_episode(self):
        pass

    def observe_reward(self, rew):
        pass
