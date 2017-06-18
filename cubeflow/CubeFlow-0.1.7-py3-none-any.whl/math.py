from typing import Iterable, Any
from math import sqrt


def l1_norm(values: Iterable[Any]) -> Any:
    """
    Calculates the l_1 norm of a sequence of values.
    :param values: Sequence of values for which __abs__ and __add__ are defined. 
    :return: l_1 norm value.  
    """
    return sum(map(abs, values))


def l2_norm(values: Iterable[Any]) -> float:
    """
    Calculates the l_2 norm of a sequence of values.
    :param values: Sequence of values for which __pow__ and __add__ are defined. 
    :return: l_2 norm value.
    """
    return sqrt(sum((x*x for x in values)))


def square(value: float) -> float:
    """
    Calculates the square of a number. Same as value**2.
    :param value: floating point number to be squared.
    :return: square of value.
    """
    return value*value
