# coding=utf-8
# Filename: k40.py
# pylint: disable=locally-disabled
"""
A collection of k40 related functions and modules.

"""
from __future__ import division, absolute_import, print_function

from scipy import constants
import numpy as np


import km3pipe as kp


def triggered_hits(blob):
    hits = blob['Hits']
    return hits[hits.triggered]


class HitProjector(kp.Module):
    def configure(self):
        self.t0 = self.get('t0') or None
        self.pos0 = self.get('pos0') or np.array([0, 0, 117.2])
        self.n = self.get('n') or 1.35

    def process(self, blob):
        hits = blob['Hits'].triggered_hits
        if self.t0 is None:
            t0 = np.min(hits.time)
        timediff = hits.time - t0
        pos = hits.pos
        dir_xyz = hits.dir
        posdiff = pos - self.pos0
        dt = timediff * 1e9 * constants.c / self.n
        pos_proj = posdiff + dir_xyz * dt
        blob['ProjectedHitPos'] = pos_proj
        return blob
