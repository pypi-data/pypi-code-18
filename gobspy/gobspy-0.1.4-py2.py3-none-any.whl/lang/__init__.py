import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from .builtins import builtins
from .state import state
from .preprocessor import preprocess
from .board import Board
from traceback import format_exc

class GobspyResult:

    def __init__(self, pycode, out, final_board, error=''):
        self.final_board = final_board
        self.out = out
        self.result = []
        self.pycode = pycode
        self.error = error

    def failed(self):
        return self.final_board is None

class Gobspy:

    def run(self, text, filepath=None, initial_board=None):
        state.init()
        if initial_board:
            state.board = initial_board
        code = preprocess(text)
        old_output = sys.stdout
        redirected_output = sys.stdout = StringIO()

        final_board = None
        error_message = ''
        try:
            exec(code, builtins, builtins)
            final_board = state.board
        except Exception as e:
            error_message = format_exc(e).replace('<string>', filepath)
        sys.stdout = old_output
        result = GobspyResult(code, redirected_output.getvalue(), final_board, error_message)
        return result

Gobstones = Gobspy

run = lambda *args, **kwargs: Gobspy().run(*args, **kwargs)
