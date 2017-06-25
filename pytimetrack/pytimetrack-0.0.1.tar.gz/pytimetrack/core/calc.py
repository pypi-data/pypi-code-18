#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
from typing import List, Tuple

class CalcTrack(object):

    def __init__(self, span: float = 24.0, sequence: float = 6.0):
        self.span_ = span * 3600.0
        self.seq_ = sequence * 3600.0

    def delta(self, ts: datetime.datetime, te: datetime.datetime) -> int:
        tt = te - ts
        return tt.total_seconds()

    def calc(self, times: List[datetime.datetime]) -> List[Tuple[datetime.datetime, datetime.datetime]]:
        tracks = []
        time_series = sorted(times)
        ts = time_series[0]
        for idx, time in enumerate(time_series):
            if idx < len(times) - 1:
                dt_span, dt_seq = self.delta(ts, time_series[idx+1]), self.delta(time, time_series[idx+1])
                if dt_span > self.span_ or dt_seq > self.seq_:
                    track = (ts, time)
                    tracks.append(track)
                    ts = time_series[idx+1]
                else:
                    pass
            else:
                track = (ts, time)
                tracks.append(track)
        return tracks
