#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd

from typing import List, Tuple

from .model import CurvatureModel
from ..core.curvature import Curvature as CurvatureCore
from ..wrapper.pandas import fit_dataframe_wrapper

class Curvature(CurvatureCore):

    @fit_dataframe_wrapper
    def fit(self, X: List[Tuple[float, float]]) -> CurvatureModel:
         core_model = super().fit(X)
         return CurvatureModel(core_model.curvs_, core_model.coefs_)
