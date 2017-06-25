#!/usr/bin/env python
# -*- coding:utf-8 -*-

from typing import Callable, List

import pandas as pd
from ..core.curvature import Curvature
from ..core.model import CurvatureModel

def fit_dataframe_wrapper(func: Callable[[Curvature, List[float]], CurvatureModel]) -> Callable[[Curvature, pd.core.frame.DataFrame, str], CurvatureModel]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, featureCols: List[str] = ["features"]) -> CurvatureModel:
        features = dataframe[featureCols].values.tolist() if len(featureCols) > 1 else dataframe[featureCols[0]].values.tolist()
        return func(self, features)
    return _wrap

def predict_dataframe_wrapper(func: Callable[[Curvature, List[float]], List[float]]) -> Callable[[Curvature, pd.core.frame.DataFrame, str], pd.core.frame.DataFrame]:
    import functools
    @functools.wraps(func)
    def _wrap(self, dataframe: pd.core.frame.DataFrame, thresholds: List[float] = [0.0], predictCol: str = "labels") -> pd.core.frame.DataFrame:
        predictions = func(self, thresholds)
        newframe = pd.Series(predictions, index=dataframe.index.tolist(), name=predictCol)
        return pd.concat([dataframe, newframe], axis=1)
    return _wrap
