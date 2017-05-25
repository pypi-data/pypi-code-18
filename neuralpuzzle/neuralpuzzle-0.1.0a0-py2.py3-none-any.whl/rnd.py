# -*- coding:utf-8 -*-
"""
A module with a package-wide rndom number generator,
used for weight initialization and seeding noise layers.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


_rnd = np.random

def get_rnd():
    """
    Returns
    -------
    :class:`np.rndom.rndomState` instance
    """
    return _rnd


def set_rnd(new_rnd):
    """
    Parameters
    ----------
    new_rnd : `np.rndom` or a :class:`np.rndom.rndomState` instance
    """
    global _rnd
    _rnd = new_rnd
