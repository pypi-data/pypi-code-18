# encoding=utf8


"""
Module containing functions for performing set operations

"""


import numpy as np
from mathpy._lib import _create_array


def iselement(x, a):
    a = _create_array(a)[0]

    if x in a:
        return True
    else:
        return False


def issubset(a, b):
    a, b = _create_array(a)[0], _create_array(b)[0]

    for i in a:
        if i not in b:
            return False

    return True


def union(a, b):
    u = a.copy()
    a, b = _create_array(a)[0], _create_array(b)[0]

    for i in np.arange(len(b)):
        if b[i] not in a:
            u.append(b[i])

    return u


def intersection(a, b):
    a, b = _create_array(a)[0], _create_array(b)[0]

    if len(a) > len(b):
        c = len(a)
    else:
        c = len(b)

    intersect = []

    for i in np.arange(c):
        if a[i] not in b:
            intersect.append(a[i])

    return intersect


def equalsets(a, b):
    a, b = _create_array(a)[0], _create_array(b)[0]

    if len(a) != len(b):
        return False

    for i in np.arange(len(a)):
        if a[i] not in b:
            return False

    return True