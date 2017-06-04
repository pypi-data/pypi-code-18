import random
__version__ = (0, 0, 5)
from .tools import benchmark, gymwrapper
__all__ = ['benchmark', '__version__', 'RandomAgent', 'gymwrapper']


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
