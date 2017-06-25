#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import pandas as pd

from typing import List

from .model import TrackModel
from ..core.track import Track as TrackCore
from ..wrapper.pandas import fit_dataframe_wrapper

class Track(TrackCore):

    @fit_dataframe_wrapper
    def fit(self, X: List[datetime.datetime]) -> TrackModel:
        core_model = super().fit(X)
        return TrackModel(core_model.clusters_)
