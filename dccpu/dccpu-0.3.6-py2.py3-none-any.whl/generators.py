import numpy as np
import random
from string import ascii_lowercase

# TODO: add tests
# TODO: add error checking, exceptions

letters = list(ascii_lowercase)

## Random instance generators

def rand_int(lo=0, hi=10):
    """
    Generate a random integer.

    Args:
        lo (int): lower bound, inclusive.
        hi (int): upper bound, exclusive.

    Returns:
        int: a random integer.
    """
    i = int(random.random() * (hi - lo))
    return list(range(lo, hi))[i]

def rand_float(lo=0.0, hi=10.0, precision=2):
    """
    Generate a random float to a specified precision.

    Args:
        lo (float): lower bound, inclusive.
        hi (float): upper bound, exclusive.
        precision (int): number of decimal places to round to.

    Returns:
        float: a random float.
    """
    return round(random.uniform(lo, hi), precision)

def rand_char(use_chars=''):
    """
    Generate a random letter from the alphabet or a custom list of letters.

    Args:
        user_chars (list): a comma delimited string of letters.

    Returns:
        str: a random letter from the defined alphabet.
    """
    use = use_chars.replace(' ', '').split(',') if use_chars else letters
    i = int(random.random() * (len(use)))
    return use[i]

def rand_bool():
    """
    Generate a random boolean.

    Returns:
        bool: a random boolean, True or False.
    """
    i = int(random.random() * 2)
    return [True, False][i]

def rand_none():
    """
    Generate a random NoneType object.

    Returns:
        None: a random NoneType object, e.g. empty list or empty string.
    """
    i = int(random.random() * 2)
    return [[], '', None][i]

def rand_type(exclude=[]):
    """
    Generate an instance of a random Python type, e.g. a random string or a random integer.

    Args:
        exclude (list): a list of types to exclude, denoted as strings. E.g. ['None', 'str']

    Returns:
        An instance of a random Python type.
    """
    temp = ['str', 'bool', 'int', 'float', 'None']
    for t in exclude: temp.remove(t)
    typ = temp[int(random.random() * len(temp))]

    if typ == 'str': return rand_char()
    elif typ == 'bool': return rand_bool()
    elif typ == 'int': return rand_int()
    elif typ == 'float': return rand_float()
    elif typ == 'None': return rand_none()

# Random vector generators

def int_vector(lo=0, hi=10, size=4, sort=False):
    """
    Generate a random integer vector.

    Args:
        lo (int): lower bound for random integers.

        hi (int): upper bound for random integers.

        size (int): size of the vector.
            To get a vector of a random size within a given upper bound, pass a negative integer.
            For example, to generate a vector of some size between 1 and 5, pass -5.

        sort (bool): if True, vector is sorted.

    Returns:
        list: a list of random integers.
    """
    # TODO: add an arg to get just evens or odds in a range
    n = rand_int(1, -size) if size < 0 else size
    res = [int(random.random() * (hi - lo)) for _ in range(n)]
    if sort: res.sort()
    return res

def float_vector(lo=0.0, hi=10.0, size=4, sort=False, precision=2):
    """
    Generate a random float vector.

    Args:
        lo (float): lower bound for random floats.

        hi (float): upper bound for random floats.

        size (int): size of the vector.
            To get a vector of a random size within a given upper bound, pass a negative integer.
            For example, to generate a vector of some size between 1 and 5, pass -5.

        sort (bool): if True, vector is sorted.

        precision (int): number of decimal places to round vector elements to.

    Returns:
        list: a list of random floats.
    """
    n = rand_int(1, -size) if size < 0 else size
    res = [round(random.uniform(lo, hi), precision) for _ in range(n)]
    if sort: res.sort()
    return res

def char_vector(size=4, sort=False, use_chars=None):
    """
    Generate a random character vector.

    Args:
        size (int): size of the vector.
            To get a vector of a random size within a given upper bound, pass a negative integer.
            For example, to generate a vector of some size between 1 and 5, pass -5.

        sort (bool): if True, vector is sorted.

        use_chars (string): override the letters used by passing a comma delimited string, e.g. 'a, b, c'
            If len(use_chars) < size, there will be guaranteed repeated elements.

    Returns:
        list: a list of random characters.
    """
    n = rand_int(1, -size) if size < 0 else size
    use = use_chars.replace(' ', '').split(',') if use_chars else letters
    res = [use[int(random.random() * (len(use)))] for _ in range(n)]
    if sort: res.sort()
    return res

def rand_vector(size=4, exclude=[]):
    """
    Generate a vector of random objects.

    Args:
        size (int): size of the vector.
            To get a vector of a random size within a given upper bound, pass a negative integer.
            For example, to generate a vector of some size between 1 and 5, pass -5.

        exclude (list): a list of types to exclude, denoted as strings. E.g. ['None', 'str']

    Returns:
        list: a list of random objects.
    """
    n = rand_int(1, -size) if size < 0 else size
    return [rand_type(exclude) for _ in range(n)]

def bool_vector(size=4, sort=False):
    """
    Generate a random boolean vector.

    Args:
        size (int): size of the vector.
            To get a vector of a random size within a given upper bound, pass a negative integer.
            For example, to generate a vector of some size between 1 and 5, pass -5.

        sort (bool): if True, vector is sorted.

    Returns:
        List of booleans.
    """
    n = rand_int(1, -size) if size < 0 else size
    res = [int(random.random() * 2) for x in range(n)]
    if sort: res.sort()
    return res

def rand_slice(lo=1, hi=5, sli=False):
    """
    Generates a random slice.

    Args:
        lo (int): lower bound for slice.

        hi (int): upper bound for slice.

        sli (bool):
            If True, function returns something of the shape: n:n, where n can only be integers.
            If False, function returns something of the shape: *x:x* where x can be integers or ':', and * can be some type of bracket.

    Returns:
        A random slice.
    """
    #TODO: maybe allow negative slicing explicitly
    if sli:
        _lo = rand_int(lo, hi - 1)
        _hi = rand_int(_lo + 1, hi)
        return _slice(_lo, _hi)
    else:
        intervals = ['o', 'ho', 'hc', 'c']
        # ':' is a valid index for intervals but not for slices e.g. '2:3' as defined in _slice and explained in docstring.
        _lo = rand_int(lo, hi - 1)
        _hi = rand_int(_lo + 1, hi)
        return random.choice([_slice(_lo, _hi, typ=i) for i in intervals])

def rand_list_perm(var_list=None):
    """
    Generates a random list permutation.

    Args:
        var_list (str): list of variables as a comma separated string, e.g. 'a, b, c'.
    """
    variables = [v.strip() for v in var_list.split(',')]
    random.shuffle(variables)
    return str(variables).replace('\'', '')

def int_matrix(lo=0, hi=10, nrows=2, ncols=2):
    """
    Generate a random integer matrix.

    Args:
        lo (int): lower bound for random integers.

        hi (int): upper bound for random integers.

        nrows (int): number of nrows for the matrix.

        ncols (int): number of columns for the matrix.

    Returns:
        Numpy matrix of random integers.
    """
    return np.matrix(np.random.randint(lo, hi, size=(ncols, nrows)))

def float_matrix(lo=0.0, hi=10.0, nrows=2, ncols=2, precision=2):
    """
    Generate a random float matrix.

    Args:
        lo (float): lower bound for random floats.

        hi (float): upper bound for random floats.

        nrows (int): number of nrows for the matrix.

        ncols (int): number of columns for the matrix.

    Returns:
        Numpy matrix of random floats.
    """
    temp = np.random.uniform(lo, hi, size=(ncols, nrows))
    matrix = np.round(np.matrix(temp), precision)
    return matrix

## Private Functions

def _slice(lo=0, hi=2, typ='s'):
    """
    Generate a slice, as a string.

    Args:
        lo (int): lower bound for slice index.
        hi (int): upper bound for slice index.
        typ (str):
            's': slice, e.g. 0:1
            'o': open interval, e.g. (0, 1)
            'ho': half open interval, e.g. (0, 1]
            'hc': half closed interval, e.g. [0, 1)]
            'c': closed interval, e.g. [0, 1]

    Returns:
        str: a slice or an interval, depending.
    """
    interval_dict = {
        's':'{}:{}',
        'o':'({}, {})',
        'ho':'({}, {}]',
        'hc':'[{}, {})',
        'c':'[{}, {}]'
    }

    return interval_dict[typ].format(lo, hi)

## Utility Functions

def stringify(function, typ='all', **kwargs):
    """
    Stringifies the result of another function.

    Args:
        function: the name of the function you want to run. The results of the function will be stringified.

        typ (string): The type of stringifcation to use.
            If 'all', entire result is stringified.
                e.g. [1, 2, 3] --> '[1, 2, 3]'

            If 'els', and result of function is iterable, elements of result are stringified.
                e.g [1, 2, 3] --> ['1', '2', '3']

        **kwargs: keyword arguments for the specified function.

    Returns:
        Stringified result of the passed function.
    """
    res = function(**kwargs)

    if isinstance(res, str):
        return '"{}"'.format(res)

    # res is not a string, and is iterable
    if hasattr(res, '__iter__'):
        if typ == 'els':
            return ['"{}"'.format(el) for el in res]
        else:
            return '"{}"'.format(res)

    else:
        return '"{}"'.format(res)
