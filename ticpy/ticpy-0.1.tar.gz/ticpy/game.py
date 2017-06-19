"""
This module is responsible for Game object and state as player play their turn 
"""
from __future__ import print_function
from ticpy.board import Board
from ticpy.constants import GAME_STATE, SEED, get_player_name
from random import choice
from itertools import product

try:
    input = raw_input
except NameError:
    pass


class Game(object):
    """ 
    This class is responsible for managing game state and player's turn
      
    """
    def __init__(self, rows, cols):
        """
        :param rows: (int) 
        :param cols: (int)
        """
        self._board = Board(rows, cols)
        self._current_state = None
        self._current_player = None
        self.initialize()

    def initialize(self):
        """
        Initializes the board
        :return: 
        """
        self._board.clear()
        self._current_player = choice([SEED.CROSS, SEED.NOUGHT])
        self._current_state = GAME_STATE.PLAYING

    def play(self):
        """
        Keeps asking for the input from user until game is concluded (Draw or Won)
        :return: 
        """
        while self._current_state == GAME_STATE.PLAYING:
            self.player_move(self._current_player)
            print (self._board)
            self.update_game(self._current_player)

            if self._current_state == GAME_STATE.CROSS_WON:
                print('X Won !')
            elif self._current_state == GAME_STATE.NOUGHT_WON:
                print('O Won !')
            elif self._current_state == GAME_STATE.DRAW:
                print('It is Draw !!')
            self._current_player = SEED.CROSS if self._current_player == SEED.NOUGHT else SEED.NOUGHT

    def player_move(self, seed):
        """
        Keeps asking for input until it gets the right input from user 
        :param seed: 
        :return: 
        """
        valid_input = False
        player_name = get_player_name(seed)
        while not valid_input:
            user_choice = input(player_name + ", which square? (e.g. 2B, 2b, B2 or b2) ")

            if Game.is_valid(user_choice) and self.is_available(user_choice):
                row, col = Game.get_row_col(user_choice)
                self._board.cells[row][col].content = seed
                self._board.current_row = row
                self._board.current_col = col
                valid_input = True
            else:
                print(user_choice + " is not valid. Try again...")

    def update_game(self, seed):
        """
        After player's input updates the state of game
        :param seed: 
        :return: 
        """
        if self._board.has_won(seed):
            self._current_state = GAME_STATE.CROSS_WON if seed == SEED.CROSS else GAME_STATE.NOUGHT_WON
        elif self._board.is_draw():
            self._current_state = GAME_STATE.DRAW

    @staticmethod
    def is_valid(user_choice):
        """
        Checks if user input is valid 
        :param user_choice: 
        :return: 
        """
        normalized_choice = ''.join(sorted(user_choice.lower()))
        list_of_valid_choices = map(lambda x: str(x[0]) + str(x[1]), list(product([1, 2, 3], ['a', 'b', 'c'])))

        return normalized_choice in list_of_valid_choices

    def is_available(self, user_choice):
        """
        checks if player's choice of box is available to fill in.
        :param user_choice: 
        :return: 
        """
        row, col = Game.get_row_col(user_choice)
        return self._board.cells[row][col].content == SEED.EMPTY

    @staticmethod
    def get_row_col(user_choice):
        """
        Given a user_choice returns the row and column number corresponding to it 
        :param user_choice: 
        :return: 
        """
        normalized_choice = ''.join(sorted(user_choice.lower()))
        return int(normalized_choice[0])-1, ord(normalized_choice[1])-ord('a')


def main():
    """
    Entry-point for the Game
    :return: 
    """
    # TODO: Take command line parameters for game's board size
    game = Game(3, 3)
    game.play()


if __name__ == '__main__':
    main()
