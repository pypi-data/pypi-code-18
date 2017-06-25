#!/usr/bin/env python
# -*- coding:utf-8 -*-

import math
import numpy as np
from typing import List, Tuple

class CalcCurvature(object):

    def __init__(self, npo: int = 1):
        self.npo_ = npo

    def theta(self, x: List[float], y: List[float], i_cen: int):
        v_x = np.array([x[0]-x[i_cen], y[0]-y[i_cen]])
        v_y = np.array([x[-1]-x[i_cen], y[-1]-y[i_cen]])
        norm_x = np.linalg.norm(v_x)
        norm_y = np.linalg.norm(v_y)
        inner_product = np.dot(v_x, v_y)
        if norm_x == 0 or norm_y == 0:
            return np.nan
        else:
            cos = inner_product / (norm_x*norm_y)
            if cos > 1.0000000000000001 or cos < -1.0000000000000001:
                return 0.0
            else:
                rad = np.arccos(cos)
                return rad * 180.0 / np.pi

    def sign(self, x: List[float], y: List[float], i_cen: int):
        return (x[0] - x[i_cen]) * (y[-1] - y[i_cen]) - (y[0] - y[i_cen]) * (x[-1] - x[i_cen])

    def modeling(self, x: List[float], y: List[float]):
        sumx = sum(x)
        sumy = sum(y)
        sumx2 = sum([x_i ** 2 for x_i in x])
        sumy2 = sum([y_i ** 2 for y_i in y])
        sumxy = sum([x_i * y_i for x_i, y_i in zip(x, y)])

        F = np.array([[sumx2, sumxy, sumx],
                      [sumxy, sumy2, sumy],
                      [sumx, sumy, len(x)]])

        G = np.array([[-sum([x_i ** 3 + x_i*y_i ** 2 for x_i, y_i in zip(x, y)])],
                      [-sum([x_i ** 2 *y_i + y_i ** 3 for x_i, y_i in zip(x, y)])],
                      [-sum([x_i ** 2 + y_i ** 2 for x_i, y_i in zip(x, y)])]])
        try:
            T = np.linalg.solve(F, G)
        except:
            return (0, 0, float("inf"))

        cxe = float(T[0] / -2)
        cye = float(T[1] / -2)
        try:
            re = math.sqrt(cxe ** 2 + cye ** 2 - T[2])
        except:
            return (cxe, cye, float("inf"))
        return (cxe, cye, re)

    def calc(self, coords: List[Tuple[float, float]], std: int = 3):
        curvs = []
        ndata = len(coords)
        for i in range(ndata):
            lind = 0 if i - self.npo_ < 0 else i - self.npo_
            hind = ndata if i + self.npo_ + 1 >= ndata else i + self.npo_ + 1
            xs = [c[0] for c in coords[lind:hind]]
            ys = [c[1] for c in coords[lind:hind]]
            (cxe, cye, re) = self.modeling(xs, ys)
            curv = { "model": None, "value": None }
            if len(xs) >= std:
                cind = int((len(xs)-1)/2.0)
                if self.theta(xs, ys, cind) == 180.0:
                    curv["value"] = 0.0
                elif self.sign(xs, ys, cind) > 0:
                    curv["value"] = 1.0/-re
                else:
                    curv["value"] = 1.0/re
            else:
                curv["value"] = float("nan")
            curv["model"] = (cxe, cye, re)
            curvs.append(curv)
        return curvs
