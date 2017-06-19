import random


class MCAgent:
    def __str__(self):
        return 'Monte Carlo Agent'

    def __init__(self, actions, ep=0.95):
        self.actions = actions
        self.ep = ep
        self.reset()

    def reset(self):
        self.totals = {}
        self.counts = {}
        self.means = {}
        self.lastobs = None
        self.lastact = None

    def copy(self):
        d = MCAgent(self.actions, self.ep)
        d.totals = self.totals
        d.counts = self.counts
        d.means = self.means
        d.lastobs = self.lastobs
        d.lastact = self.lastact
        return d

    def get_action(self, observation):
        if isinstance(observation, list):
            observation = tuple(observation)
        if observation not in self.means:
            self.means[observation] = {a: 0 for a in self.actions}
            self.totals[observation] = {a: 0 for a in self.actions}
            self.counts[observation] = {a: 1 for a in self.actions}
        if random.random() <= self.ep:
            vals = [(v, a) for a, v in self.means[observation].items()]
            vals.sort(key=lambda x: x[0])
            act = vals[-1][1]
        else:
            act = random.choice(self.actions)
        self.lastobs = observation
        self.lastact = act
        return act

    def start_episode(self):
        pass

    def end_episode(self):
        # Recalculate means
        for obs in list(self.totals.keys()):
            self.means[obs] = {a: (self.totals[obs][a]/self.counts[obs][a])
                               for a in self.actions}

    def observe_reward(self, rew):
        self.totals[self.lastobs][self.lastact] += rew
        self.counts[self.lastobs][self.lastact] += 1
