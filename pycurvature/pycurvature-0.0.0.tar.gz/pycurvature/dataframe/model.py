#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd

from typing import List

from ..core.model import CurvatureModel as CurvatureModelCore
from ..wrapper.pandas import predict_dataframe_wrapper

class CurvatureModel(CurvatureModelCore):

    @predict_dataframe_wrapper
    def predict(self, thresholds: List[float]) -> List[int]:
        return super().predict(*thresholds)
