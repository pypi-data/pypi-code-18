"""puzzle.py

This module represents the puzzle
"""

__title__ = 'puzcw'
__author__ = 'Brian Wu'
__author_email__ = 'brian.george.wu@gmail.com'

import urllib2
from datetime import datetime, timedelta
import math
import puz

from box import Box
from clues import Clue, Clues, ACROSS_ID, DOWN_ID
from image import CrosswordImage
from exception import BoardDimensionException, \
    WriteException

NULL = '\x00'
CIRCLE = '\x80'
OPEN_BOX = '-'
BLANK = '.'
BOARD_START_KEY = OPEN_BOX*3
BOARD_IDX_KEY = 'NY Times'


class Crossword(object):

    def __init__(self):
        # Initialize empty game
        self.title = ''
        self.author = ''
        self.width = None
        self.height = None
        self.board = []
        self.clues = Clues()

    @classmethod
    def from_url(cls, url):
        res = urllib2.urlopen(url)
        game_str = res.read()
        return cls.from_str(game_str)

    @classmethod
    def from_str(cls, game_str):
        instance = cls()
        instance._load_data(game_str)
        return instance

    def _load_data(self, game_str):
        """ 
        Process the board string the board string. 

        1. Determine index of board start
        2. Determine n
        3. Create board and boxes
        """
        p = puz.load(game_str)
        print p.__dict__.keys()

        # Get basic info
        self.width = p.width
        self.height = p.height
        self.title = p.title
        self.author = p.author

        # Get important vals
        fill = p.fill
        solution = p.solution
        clues = p.clues
        circ = p.extensions['GEXT'] if (p.extensions and 'GEXT' in p.extensions) else None 

        idx = 0
        clue_idx = 0
        clue_count = 1
        for row in range(self.height):
            new_row = []
            for col in range(self.width):

                # Get box info
                is_blank = fill[idx] == BLANK
                is_circle = circ and circ[idx] == CIRCLE
                answer = None if is_blank else solution[idx]
                is_across = not is_blank and \
                            (col==0 or new_row[col-1].is_blank)
                is_down = not is_blank and \
                            (row==0 or self.board[row-1][col].is_blank)

                # Determine if box has number
                if is_across or is_down:
                    number = clue_count
                    if is_across:
                        clue = Clue(clue=clues[clue_idx],
                                    start_position=(row,col),
                                    num=clue_count,
                                    clue_type=ACROSS_ID)
                        self.clues.put(clue_count, ACROSS_ID, clue)
                        clue_idx += 1
                    if is_down:
                        clue = Clue(clue=clues[clue_idx],
                                    start_position=(row,col),
                                    num=clue_count,
                                    clue_type=DOWN_ID)
                        self.clues.put(clue_count, DOWN_ID, clue)
                        clue_idx += 1
                    clue_count += 1
                else:
                    number = None

                # Create and append box             
                box = Box(answer=answer,
                          is_blank=is_blank,
                          number=number,
                          is_circle=is_circle)
                new_row.append(box)
                idx += 1

            self.board.append(new_row)

    def save_game(self):
        """ Save crossword as image, return path. """
        image = CrosswordImage(self.width, self.height, self.board)
        image.construct_image()
        return image.save()

    def get_clue(self, num, clue_type):
        """ Retrieve clue by key. """
        num = int(num)
        clue_type = clue_type.lower()
        try:
            return self.clues.get_clue(num, clue_type)
        except KeyError:
            return "Clue %s:%s doesn't exist!" % (num, clue_type)

    @property
    def across_clues(self):
        """ Retrieve all across clues. """
        return self.clues.clues_by_type(ACROSS_ID)

    @property
    def down_clues(self):
        """ Retrieve all down clues. """
        return self.clues.clues_by_type(DOWN_ID)

    @property
    def all_clues(self):
        return self.across_clues + self.down_clues

    def _write(self, num, clue_type, word, guess_type):
        clue = self.get_clue(num, clue_type)
        x, y = clue.start_position
        for letter in word:
            box = self.board[x][y]

            # Raise WriteException for blank box
            if box.is_blank: raise WriteException

            box.write(guess_type, clue_type, letter.upper())

            # Increment x or y
            if clue_type == ACROSS_ID:
                y += 1
            else:
                x += 1

        # Mark clue as submitted
        if guess_type == 'submission':
            clue.submitted = True

    def submit(self, num, clue_type, word):
        self._write(num, clue_type, word, 'submission')

    def ghost(self, num, clue_type, word):
        self._write(num, clue_type, word, 'ghost')

    def clear(self, num, clue_type):
        """ Clear answers from boxes by direction. """
        clue = self.get_clue(num, clue_type)
        x, y = clue.start_position
        while True:
            try:
                box = self.board[x][y]
                if box.is_blank: raise WriteException
                box.clear(clue_type)
                if clue_type == ACROSS_ID:
                    y += 1
                else:
                    x += 1

            # Break at a blank or index error
            except (WriteException, IndexError) as e:
                clue.submitted = False
                break
