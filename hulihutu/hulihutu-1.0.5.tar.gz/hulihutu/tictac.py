"""
    Tictac
"""

import numpy as np


class Tictac:
    """
        Tictac module
        circle is 1, cross is -1
        reward for circle win is 1,
        reward for cross win or draw is -1
    """

    def __init__(self):
        self.ended = False
        self.board = np.zeros([3, 3], np.int8)
        self.color = 1
        self.winner = 0

    def search_possible_steps(self):
        """search possible steps, return all steps available as an array"""
        if self.ended:
            return False
        possible_steps_turple = (self.board == 0)
        possible_steps = np.transpose(possible_steps_turple.nonzero())
        return possible_steps

    def get_next_states(self):
        """get possible steps"""
        if self.ended:
            return False
        possible_steps = self.search_possible_steps()
        #next_color = self.color * -1
        n = possible_steps.shape[0]
        next_states = np.zeros([n, 3, 3], dtype=np.int8)
        for i in range(n):
            x, y = possible_steps[i]
            next_states[i][x][y] = self.color
            next_states[i] = next_states[i] + self.board
        return next_states

    def get_reward(self, actions, next_states):
        """check one of the board, if game has ended
            define circle as 1, cross as -1
            if circle wins return reward 1
            else return reward 0
        """
        r = []
        for state in next_states:
            ended, winner = self.judge_terminal(state)
            if ended:
                r.append(winner)
            else:
                r.append(0)
        return np.array(r)

    def play(self,position):
        """play at centain position"""
        (x, y) = position
        if self.board[x][y] != 0:
            print('Error, ' + str(x) + ',' + str(y) + ' is not a possible state')
            return
        else:
            self.board[x][y] = self.color
            self.color = self.color * -1
            (terminated, winner) = self.judge_terminal()
            if terminated:
                self.ended = True
                self.winner = winner
                return winner

    def judge_terminal(self, state=False):
        """return terminal State and winner"""
        if type(state) == np.ndarray:
            board = state
        else:
            board = self.board
        diagsum1 = board[0][0] + board[1][1] + board[2][2]
        diagsum2 = board[0][2] + board[1][1] + board[2][0]
        if np.any(np.sum(board, 0) == 3) or np.any(np.sum(board, 1) == 3) \
                or diagsum1 == 3 or diagsum2 == 3:
            return (True, 1)
        elif np.any(np.sum(board, 0) == -3) or np.any(np.sum(board, 1) == -3) \
                or diagsum1 == -3 or diagsum2 == -3:
            return (True, -1)
        elif np.all(board != 0):
            return (True, 0)
        else:
            return (False, 0)

    def print_board(self):
        """print out the board"""
        print(self.board)
    
    def set_board(board):
        """
            set board with a board object
            example: 
            {'one':1, 'five':2, 'nine':1}
        """
        

    def generate_and_store_game_by_policy(self, policy):
        """generate a game with policy"""
        while self.ended != True:
            actions = self.search_possible_steps()
            next_states = self.get_next_states()
            action = policy.pai(self.board)
            # next_state = self.play(action)
            # next_value = db.find_value(next_state)
            print(self.board)

    def reset(self):
        """reset"""
        self = self.__init__()
        return self

    def apply_policy(self, policy, method):
        """apply policy to get the next action"""
        action, optimal_value, move = policy(self, method)
        return action, optimal_value, move
