#!/usr/bin/env python

import numpy as np
import pandas as pd

from km3pipe.io.pandas import H5Chain, merge_event_ids

from km3learn.process import preprocess


def load_orca_files(fnames, precut=True, pid=False, **kwargs):
    with H5Chain(fnames) as h5c:
        if precut:
            print('read precut...')
            survives_precut = np.array(
                h5c['/pid/survives_precut'].astype('bool'))
        if pid:
            print('read pid...')
            proba = h5c['/pid/proba']
        print('read mc...')
        mc = h5c['/truth']
        print('read gandalf...')
        gand = h5c['/reco/gandalf']
        print('read rlns...')
        rlns = h5c['/reco/rlns']
        print('read thomas...')
        thom = h5c['/reco/thomas']
        print('read dusj...')
        dusj = h5c['/reco/dusj']
        print('combine...')
        rec = pd.concat((gand, rlns, dusj, thom), axis=1)
        del gand
        del rlns
        del thom
        del dusj
        rec = merge_event_ids(rec)
        del rec['event_id']

    rec, mc = preprocess(rec, mc, **kwargs)

    out = [rec, mc]

    if precut:
        out.append(survives_precut)
    if pid:
        out.append(proba)
    return out
