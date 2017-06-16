#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Y. Jia <ytjia.zju@gmail.com>

from utils_py.Point import Point


class Polygon(object):
    """
    Polygon class represents a set of points on a cartesian plane which
    form a polygon
    """

    def __init__(self, *points):
        self.points = list()
        for p in points:
            if isinstance(p, Point):
                self.points.append(p)
            elif isinstance(p,
                            dict) and 'lng' in p.keys() and 'lat' in p.keys():
                self.points.append(
                        Point(p['lng'], p['lat']))
            elif isinstance(p, (list, tuple)):
                self.points.append(Point(*p))
            else:
                raise TypeError(
                        "Points must be provided in a form of a Point class, "
                        "dictionary, list, or tuple instances. You've "
                        "provided %s instance." % p.__class__)
        if len(self.points) < 3:
            raise ValueError(
                    "The points you provided do not define a polygon.")

    def __repr__(self):
        return "[" + ", ".join(map(str, self.points)) + "]"
