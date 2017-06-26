#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from typing import List, Tuple

class CurvatureModel(object):

    def __init__(self, curvatures: List[float], coefficients: List[Tuple[float, float, float]]):
        self.curvs_ = curvatures
        self.coefs_ = coefficients

    def compare(self, s: float, lth: float, hth: float) -> int:
        if s > hth:
            return 1.0
        elif s < lth:
            return -1.0
        else:
            return 0.0

    def evaluate(self, subject: float, thresholds: List[float]) -> float:
        if math.isnan(subject):
            return subject
        else:
            label = 0.0
            iterations = int( ( len(thresholds) + 1 ) / 2 )
            for i in range(iterations):
                if len(thresholds) % 2 == 0:
                    label = label + self.compare(subject, thresholds[2*i], thresholds[2*i+1])
                else:
                    if i == 0:
                        label = label + self.compare(subject, thresholds[i], thresholds[i])
                    else:
                        label = label + self.compare(subject, thresholds[2*i-1], thresholds[2*i])
            return label

    def predict(self, *thresholds: float) -> int:
        thresholds = sorted(thresholds)
        predicts = [self.evaluate(feature, thresholds) for feature in self.curvs_]
        return predicts
