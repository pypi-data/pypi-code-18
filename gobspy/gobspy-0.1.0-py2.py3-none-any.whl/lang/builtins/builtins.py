import sys
from ..i18n import translate as t
from .types import *
from ..state import state as global_state
from ..exceptions import DynamicException

# Board Procedures

def PutStone(color):
    """Put a stone in the board."""
    if typeof(color) != 'Color':
        msg = t('The argument to PutStone should be a color')
        raise RuntimeException(msg)
    global_state.board.put_stone(color)

def TakeStone(color):
    """Take a stone from the board."""
    if typeof(color) != 'Color':
        msg = t('The argument to TakeStone should be a color')
        raise RuntimeException(msg)
    if global_state.board.num_stones(color) > 0:
        global_state.board.take_stone(color)
    else:
        msg = global_state.backtrace(
            t('Cannot take stones of color %s') % (color,))
        raise RuntimeException(msg)

def Move(direction):
    """Move the head."""
    if typeof(direction) != 'Dir':
        msg = t('The argument to Move should be a direction')
        raise RuntimeException(msg)
    if global_state.board.can_move(direction):
        global_state.board.move(direction)
    else:
        msg = global_state.backtrace(
            t('Cannot move to %s') % (direction,))
        raise RuntimeException(msg)

def GoToOrigin():
    return global_state.board.go_to_origin()

def GoToBoundary(direction):
    return global_state.board.go_to_boundary(direction)

def ClearBoard():
    return global_state.board.clear_board()

# Board Functions

def numStones(color):
    """Number of stones of the given color."""
    if typeof(color) != 'Color':
        msg = t('The argument to numStones should be a color')
        raise RuntimeException(msg)
    return global_state.board.num_stones(color)

def existStones(color):
    """Return True iff there are stones of the given color."""
    if typeof(color) != 'Color':
        msg = t('The argument to existStones should be a color')
        raise RuntimeException(msg)
    return global_state.board.exist_stones(color)

def canMove(direction):
    """Return True iff the head can move to the given direction."""
    if typeof(direction) != 'Dir':
        msg = t('The argument to canMove should be a direction')
        raise RuntimeException(msg)
    return global_state.board.can_move(direction)



# General Procedures

def Imprimir(*values):
    strings = list(map(str, values))
    print('"' + ' '.join(strings) + '"')


# General Functions

minBool  = lambda: False
maxBool  = lambda: True
minDir   = lambda: DIRECTIONS[0]
maxDir   = lambda: DIRECTIONS[-1]
minColor = lambda: COLORS[0]
maxColor = lambda: COLORS[-1]

def next(value):
    "Return the next value of the same type as the one given."
    if isinstance(value, bool):
        return not value
    elif isinteger(value):
        return value + 1
    elif isinstance(value, list):
        return [next(elem) for elem in value]
    elif isenum(value):
        return value.next()
    else:
        assert False

def prev(value):
    "Return the previous value of the same type as the one given."
    if isinstance(value, bool):
        return not value
    elif isinteger(value):
        return value - 1
    elif isinstance(value, list):
        return [prev(elem) for elem in value]
    elif isenum(value):
        return value.prev()
    else:
        assert False

def opposite(value):
    "Return the opposite value of the same type as the one given."
    if isinstance(value, bool):
        return not value
    elif isinteger(value):
        return -value
    elif isinstance(value, list):
        return [opposite(elem) for elem in value]
    elif isenum(value):
        return value.opposite()
    else:
        assert False

def ord(value):
    """Returns an integer representing the ord of the given
    Gobstones value."""
    if isinstance(value, bool):
        if value:
            return 1
        else:
            return 0
    elif isinteger(value):
        return value
    elif isenum(value):
        return value.ord()
    else:
        assert False

# Private

class RuntimeException(DynamicException):
    """Base exception for Gobstones runtime errors."""

    def error_type(self):
        "Description of the exception type."
        return t('Runtime error')

def isinteger(value):
    "Return True iff the given Python value is integral."
    if sys.version_info[0] < 3:
        return isinstance(value, int) or isinstance(value, long)
    else:
        return isinstance(value, int)

def isenum(value):
    return hasattr(value, 'ord') and hasattr(value.ord, '__call__')

def typeof(value):
    "Return the name of the type of the value."
    if isinstance(value, bool):
        return 'Bool'
    elif isinteger(value):
        return 'Int'
    elif isinstance(value, list):
        assert False
    else:
        return value.enum_type()


def define_function(_def):

    def function(*args, **kwargs):
        global_state.push()
        result = _def(*args, **kwargs)
        global_state.pop()
        return result

    return function

# Saving locals
# This line must be the last line on this file.
builtins = locals()
