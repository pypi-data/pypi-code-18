#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Y. Jia <ytjia.zju@gmail.com>

from utils_py import math_util


class Point(object):
    """
    A point on the map described with longitude and latitude.
    """

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def __repr__(self):
        return 'Point({0.lng!r}, {0.lat!r})'.format(self)

    def __str__(self):
        return '({0.lng!s}, {0.lat!s})'.format(self)

    def __eq__(self, other):
        if math_util.almost_eq(self.lng, other.lng) and math_util.almost_eq(
                self.lat, other.lat):
            return True
        else:
            return False
