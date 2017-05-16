#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Convert bytes to kilobytes, megabytes, gigabytes, etc."""


def bytes2human(bites, to, bsize=1024):
    """Convert bytes to kilobytes, megabytes, gigabytes, etc."""
    bitez, to = float(abs(bites)), str(to).strip().lower()
    for i in range({'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}[to]):
        bitez = bitez / int(abs(bsize))
    return str(int(bitez)) + {
        'k': " Kilo", 'm': " Mega", 'g': " Giga", 't': " Tera",
        'p': " Peta", 'e': " Exa"}[to] + "bytes"
