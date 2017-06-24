# -*- coding: utf-8 -*-
"""

Author
------
Bo Zhang

Email
-----
bozhang@nao.cas.cn

Created on
----------
- Sat Sep 03 16:00:00 2017

Modifications
-------------
- Sat Sep 03 12:00:00 2017

Aims
----
- plotting tools

"""


import numpy as np
import matplotlib.pyplot as plt


def plot_mse(s):
    fig, ax = plt.subplots(1, 1, figsize=(8, 6), tight_layout=True)
    plt.hist(-s.nmse[s.nmse != 0], np.linspace(0, 1, 80), histtype='step',
             lw=2, label="MSE")
    plt.hist(-s.scores[s.nmse != 0], np.linspace(0, 1, 80), histtype='step',
             lw=2, label="CV MSE")
    ylim = plt.gca().get_ylim()
    plt.vlines(np.percentile(-s.nmse[s.nmse != 0], [14, 50, 86]), *ylim,
               linestyle='--', label="14, 50, 86 percentiles")
    plt.xlim(0, 1)
    plt.ylim(*ylim)
    plt.ylabel("Counts")
    plt.xlabel("MSE")
    fig.tight_layout()
    return fig