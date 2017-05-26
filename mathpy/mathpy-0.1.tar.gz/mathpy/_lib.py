"""
Private module containing functions used throughout package.

"""

import numpy as np
import pandas as pd


def _create_rec_arrays(*args):
    recs = []

    for x in args:
        if x is None:
            continue

        if isinstance(x, pd.DataFrame):
            xn = x.to_records()
        elif isinstance(x, pd.Series):
            xn = x.to_frame().to_records()
        elif isinstance(x, list):
            xn = np.core.records.fromrecords(np.array(x))
        elif isinstance(x, dict):
            cols = ','.join(list(x.keys()))
            _xn = np.column_stack(x.values())
            xn = np.core.records.fromrecords(_xn, names=cols)
        else:
            xn = np.core.records.fromrecords(x)

        recs.append(xn)

    return recs


def _create_array(x):
    if isinstance(x, np.ndarray) is False:
        if isinstance(x, pd.DataFrame):
            cols = x.columns
            xn = x.as_matrix()
        elif isinstance(x, pd.Series):
            cols = x.name
            xn = x.to_frame().as_matrix()
        elif isinstance(x, list):
            xn = np.array(x).T
            cols = None
        elif isinstance(x, dict):
            cols = ','.join(list(x.keys))
            _xn = np.column_stack(x.values())
            xn = np.array(_xn)
        else:
            xn = np.array(x)
            cols = None
    else:
        xn = x
        cols = None

    return (xn, cols)


def _join_rec_arrays(arr):
    dtypes = []
    for a in arr:
        dtypes.append(np.sum(a.dtype.descr))
    rarray = np.empty(len(arr[0]), dtype=dtypes)
    for a in arr:
        for n in a.dtype.names:
            rarray[n] = a[n]

    return rarray
