from .board import Board
from traceback import format_stack, extract_stack, format_list

class State:

    def __init__(self):
        self.init()

    def backtrace(self, message=''):
        return message + '\n' + ''.join(format_list(extract_stack()[:-2]))

    def push(self):
        self.board.push_state()

    def pop(self):
        self.board.pop_state()

    def init(self):
        self.board = Board().randomize()

state = State()
