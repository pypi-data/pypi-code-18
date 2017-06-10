# -*- coding: UTF-8 -*-

from collections import OrderedDict

"""
Dead-simple Roman numerals <-> decimal numbers convertion.
"""

symbols = OrderedDict([x, n] for x, n in (
    ("M", 1000),
    ("D",  500),
    ("C",  100),
    ("L",   50),
    ("X",   10),
    ("V",    5),
    ("I",    1),
))

_expandings = (
    ("CM", "DCCCC"),
    ("CD", "CCCC"),
    ("XC", "LXXXX"),
    ("XL", "XXXX"),
    ("IX", "VIIII"),
    ("IV", "IIII"),
)

_reducings = tuple([(n, x) for x, n in _expandings])


def _expand(x):
    for shortx, longx in _expandings:
        x = x.replace(shortx, longx)
    return x

def _reduce(x):
    for longx, shortx in _reducings:
        x = x.replace(longx, shortx)
    return x

def roman_to_decimal(x):
    n = 0
    for c in _expand(x.upper()):
        n += symbols[c]
    return n

def decimal_to_roman(n):
    cs = []
    for x, nx in symbols.items():
        d, m = divmod(n, nx)
        n = m
        cs.append(x * d)
    return _reduce("".join(cs))
