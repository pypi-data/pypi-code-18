#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import pandas as pd

from typing import List

from ..core.model import TrackModel as TrackModelCore
from ..wrapper.pandas import predict_dataframe_wrapper

class TrackModel(TrackModelCore):

    @predict_dataframe_wrapper
    def predict(self, features: List[datetime.datetime]) -> List[int]:
        return super().predict(features)
