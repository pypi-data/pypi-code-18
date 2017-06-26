#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple

from .calc import CalcCurvature
from .model import CurvatureModel

class Curvature(CalcCurvature):

    def __init__(self, npo: int = 1):
        super().__init__(npo)

    def setNumberPoints(self, npo: int) -> object:
        self.npo_ = npo
        return self

    def getNumberPoints(self) -> int:
        return self.npo_

    def fit(self, X: List[Tuple[float, float]]) -> CurvatureModel:
        features = super().calc(X)
        curvatures = [feature[0] for feature in features]
        coefficients = [feature[1] for feature in features]
        model = CurvatureModel(curvatures, coefficients)
        return model
