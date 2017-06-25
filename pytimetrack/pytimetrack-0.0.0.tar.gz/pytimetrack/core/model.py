#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from typing import List, Tuple

class TrackModel(object):

    def __init__(self, windows: List[Tuple[datetime.datetime, datetime.datetime]]):
        self.clusters_ = windows

    def evaluate(self, subject: float) -> int:
        result = -1
        for idx, cluster in enumerate(self.clusters_):
            if cluster[0] <= subject and cluster[1] >= subject:
                result = idx
                break
            else:
                continue
        return result

    def predict(self, features: List[datetime.datetime]) -> List[int]:
        predicts = [self.evaluate(feature) for feature in features]
        return predicts
