"""
	imports
"""
from random import random
# from tictac import Tictac
from pymongo import MongoClient
import numpy as np

"""
	Markov Decision Process
	Conponents:
		state - store values
		action
		state_action pair - store rewards and quality
			reward
			q function of (s,a)
		# policies
	Retrive and Store these component to mongodb
"""


DEFAULT_REWARD = 0
DEFAULT_VALUE = 0.5
GAMMA = 0.5

""" DB interfaces """


class DB:
    """DB interface"""

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.tictac
        self.states = self.db.states
        self.actions = self.db.actions
        self.state_action = self.db.state_action
        self.statistics = self.db.statistics

    def find_state(self, state):
        """find state"""
        result = self.states.find_one({'state': state.tolist()})
        return result

    def store_state(self, state):
        """store state"""
        result = self.states.insert_one({'state': state.tolist()})
        return result

    def find_action(self, action):
        """"find action"""
        result = self.actions.find_one({'action': action.tolist()})
        return result

    def store_action(self):
        """store action"""
        pass

    def find_state_action(self, action, state):
        """find state action"""
        result = self.state_action.find_one({
            'action': action.tolist(),
            'state': state.tolist()
        })
        return result

    def store_state_action(self):
        """store state action"""
        pass

    def find_reward(self, action, state):
        """find reward"""
        result = self.state_action.find_one({
            'action': action.tolist(),
            'state': state.tolist()
        })
        return result

    def store_reward(self):
        """store reward"""
        pass

    def find_value(self, state):
        """find value"""
        value = self.find_state(state).value
        return value

    def find_values(self, states, default_value):
        """get values"""
        v = []
        for state in states:
            result = self.find_state(state)
            if result and 'value' in result:
                value = result['value']
                v.append(value)
            else:
                v.append(default_value)
        return np.array(v)

    def update_value(self, state, value):
        """store value"""
        self.states.update_one({
            'state': state.tolist()
        }, {
            '$set': {
                'value': value
            }
        }, upsert=True)
        return 0

    # def get_next_state(self, state, action):
    #     """get next state"""
    #     pass

    # def get_next_states(self, state, actions):
    #     """get next states"""
    #     pass

    # def get_next_actions(self, state):
    #     """get next actions"""
    #     return 0


class Policy:
    """define the policy"""

    def __init__(self, gamma, tao, db, default_value):
        self.gamma = gamma or 0.9
        self.tao = tao or 0.1
        self.db = db
        self.default_value = default_value

    def pai(self, tictac, method='max'):
        """given a state s and actions collection A, calculate the right action a"""
        # at some rate select random action
        # return optimal policy otherwise
        if tictac.ended:
            return False
        else:
            actions = tictac.search_possible_steps()
            next_states = tictac.get_next_states()
            rewards = tictac.get_reward(actions, next_states)
            next_states_values = self.db.find_values(
                next_states, default_value=self.default_value)
            if random() < self.tao:
                random_index = int(actions.shape[0] * random())
                value = bellman_quality_equation(rewards[random_index], self.gamma,
                                                 next_states_values[random_index])
                return (actions[random_index], value, 'explotary')
            else:
                # terminal_results = []
                # next_state_is_terminal = False
                # # for every next state which will be ended, update value and reward
                # for index, state in enumerate(next_states):
                #     ended, winner = tictac.judge_terminal(state)
                #     if ended:
                #         next_state_is_terminal = True
                #         terminal_results.append({
                #             'index': index,
                #             'winner': winner
                #         })
                (action_index, optimal_quality) = bellman_value_equation(
                    rewards, self.gamma, next_states_values, method)
                next_actions = actions[action_index]
                # select a random optimal action
                random_index = int(next_actions.shape[0] * random())
                return (next_actions[random_index], optimal_quality, 'explantary')


# Value Network


def bellman_quality_equation(reward, gamma, next_state_value):
    """
            Bellman quality equation, simplified version
            Q(s,a) = R(s,a) + gamma * simga(T(s, a, s') * V(s'))
    """
    return reward + gamma * next_state_value


def bellman_value_equation(rewards, gamma, next_states_values, method='max'):
    """
            compute Bellman value function for the given state and actions
            V(s) = max of a(R(s,a) + gamma * sigma(T(s, a, s') * V(s')))
    """
    qualities = rewards + gamma * next_states_values
    if method == 'max':
        optimal_quality = np.max(qualities)
        action_index = np.argwhere(qualities == np.max(qualities)).flatten()
    elif method == 'min':
        optimal_quality = np.min(qualities)
        action_index = np.argwhere(qualities == np.min(qualities)).flatten()
    return (action_index, optimal_quality)


class Statistics:
    """Statistics Class"""

    def __init__(self, db, policy_tag, gamma, tao, opponent_policy):
        """init get db instance"""
        self.db = db
        self.policy_tag = policy_tag
        self.gamma = gamma
        self.tao = tao
        self.opponent_policy = opponent_policy

    def summary(self):
        """return summary"""
        pass

    def count_total_states(self):
        """return total states number"""
        return self.db.states.count({})

    def count_zero_value(self):
        """count_zero_value"""
        return self.db.states.find({'value': 0}).count()

    def count_greater_than_zero(self):
        return self.db.states.find({'value': {'$gt': 0}}).count()

    def count_less_than_zero(self):
        return self.db.states.find({'value': {'$lt': 0}}).count()

    def count_eq_one(self):
        return self.db.states.count({'value': {'$eq': 1}})

    def count_eq_minus_one(self):
        """count equal minus one"""
        return self.db.states.count({'value': {'$eq': -1}})

    def count_all(self):
        """for all possible value count the number"""
        # all_values_count = {}
        # for i in range(-1, 2):
        #     if i:
        #         for j in range(9):
        #             all_values_count[i * (self.gamma ** j)] = self.db.states.count({
        #                 'value': {
        #                     '$eq': i * (self.gamma ** j)}})
        #     else:
        #         all_values_count[0] = self.count_zero_value()
        # return all_values_count
        result = self.db.states.aggregate({
            '$group': {
                '_id': '$value',
                'count': {'$sum': 1}
            }
        }, {
            '$match': {
                '_id': {'$ne': 'null'},
                'count': {'$gt': 1}
            }
        })
        return result

    def init_store(self):
        """store policy"""
        inserted_id = self.db.statistics.insert({
            'policy': self.policy_tag,
            'tao': self.tao,
            'gamma': self.gamma,
            'opponent_policy': 'optimal | random'
        })
        return inserted_id

    def sample_per_step(self, steps, interval):
        """sample per steps"""
        if steps % interval:
            self.db.statistics.update({
                'policy': self.policy_tag
            })
