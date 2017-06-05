import random
from copy import deepcopy


class QLAgent:
    def copy(self):
        return deepcopy(self)

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def __str__(self):
        return 'QLearner'

    def __init__(self, actions, lr=0.1, df=0.9, ep=0.95):
        """
        actions     : Set of actions available to the agent
        lr          : Learning Rate. `alpha` in literature.
        df          : Discount factor. `gamma` in literature.
        ep          : Epsilon. Used to control what % of the time the algorithm
                      is greedy
        """
        # actions = [0, 1, 2, 3]
        self.actions = actions
        self.lr = lr
        self.df = df
        self.ep = ep
        self.reset()

    def reset(self):
        self.q_table = dict()
        self.prev_state = None
        self.prev_action = None

    def get_action(self, state):
        state = tuple(state)
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}
        # ----------------------
        if random.random() > self.ep:
            # take random action
            action = random.choice(self.actions)
        else:
            # take action according to the q function table
            state_actions = [(v, k) for k, v in self.q_table[state].items()]
            state_actions.sort()  # Sorts in Ascending
            action = state_actions[-1][1]
        # ----------------------  set variables
        self.prev_state, self.prev_action = state, action
        # ----------------------
        return action

    def observe_reward(self, reward):
        if self.prev_state not in self.q_table:
            self.q_table[self.prev_state] = {a: 0.0 for a in self.actions}
        # ---------------------- LEARN
        if self.prev_state is not None:
            q_1 = self.q_table[self.prev_state][self.prev_action]
            q_2 = reward + self.df*max(self.q_table[self.prev_state].values())
            v = q_2 - q_1
            self.q_table[self.prev_state][self.prev_action] += self.lr*v

    def end_episode(self):
        pass

    def start_episode(self):
        pass
