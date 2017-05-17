import collections

def first(x):
    """Return the first element of x if it is iterable, else return x."""
    try:
        return x[0]
    except:
        return x

def second(x):
    """Return the second element of x."""
    if not isinstance(x, collections.Iterable):
        raise Exception('{} is not iterable.'.format(x))

    if not len(x) >= 2:
        raise Exception('{} does not have a second element.'.format(x))

    return x[1]


def last(x):
    """Return the last element of x if it is iterable, else return x."""
    try:
        return x[-1]
    except:
        return x


def rest(x):
    """Return everything after the first element of x."""
    try:
        return x[1:]
    except:
        return []
    

def butlast(x):
    """Return everything but the last element of x."""
    try:
        return x[0:-1]
    except:
        return []

# * Wrapped functions
import scipy.optimize.fsolve as _fsolve

def fsolve(objective, x0):
    ans, info, flag, msg = _fsolve(objective, x0, full_output=1)
    if flag != 1:
        raise Exception('fsolve did not finish cleanly: {}'.format(msg))

    if len(ans) == 1:
        return float(ans)
    else:
        return ans
