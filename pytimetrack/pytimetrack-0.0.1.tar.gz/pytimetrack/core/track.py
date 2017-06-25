#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from typing import List

from .calc import CalcTrack
from .model import TrackModel

class Track(CalcTrack):

    def __init__(self, span: float = 24.0, sequence: float = 6.0):
        super().__init__(span, sequence)

    def setSpan(self, span: float) -> object:
        self.span_ = span
        return self

    def setSequence(self, sequence: float) -> object:
        self.seq_ = sequence
        return self

    def getSpan(self) -> float:
        return self.span_

    def getSequence(self) -> float:
        return self.seq_

    def fit(self, X: List[datetime.datetime]) -> TrackModel:
        tracks = super().calc(X)
        model = TrackModel(tracks)
        return model
