# -*- coding: utf-8 -*-
from numpy import all, asanyarray, empty, isclose, vstack, where


__all__ = ['GlobalPointList']


class GlobalPointList(object):

    def __init__(self, rtol=1e-05, atol=1e-08):
        self.points = empty([0, 3])
        self.rtol = rtol
        self.atol = atol

    def _add_point(self, point):
        self.points = vstack((self.points, asanyarray(point)))

    def get_point_id(self, point):
        potential_ids = where(all(
            isclose(point, self.points, rtol=self.rtol, atol=self.atol),
            axis=1))[0]
        if len(potential_ids) == 0:
            id_ = len(self.points)
            self._add_point(point=point)
        elif len(potential_ids) == 1:
            id_ = potential_ids[0]
        else:
            raise ValueError((
                'Several points close to {} have been found. This may be due '
                'to changing the tolerances inbetween or manually adding a '
                'point.').format(point))
        return id_

