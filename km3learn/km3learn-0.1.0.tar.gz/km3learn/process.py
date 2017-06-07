#!/usr/bin/env python

import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

from km3pipe.mc import pdg2name, geant2pdg
from km3flux.weights import add_weights_and_fluxes

from km3learn.label import TargetGen, target_to_name


def g2p(row):
    # mupage has geant codes...
    return geant2pdg(row['type'])


def t2f(row):
    return pdg2name(row['type'])


def make_flavor(df):
    df.loc[~df.is_neutrino, 'type'] = df.apply(g2p, axis=1)
    df['flavor'] = df.apply(t2f, axis=1).astype('str')
    return df


def make_target(df):
    if 'flavor' not in df.columns:
        raise KeyError("make_target needs `flavor` column!")
    tg = TargetGen(df.type, df.is_cc)
    df['target'] = tg.track_cscd_rest
    df['antimu'] = tg.is_neutrino
    return df


def strange_flavor_to_mupage(df, fill='mu+'):
    mask = ((df.flavor == 'N/A') | (df.flavor == 'n'))
    df.loc[mask, 'flavor'] = fill
    return df


def preprocess(rec, mc, remove_nan=True, rescale=False, remove_constant=False,
               add_flavor=True, add_target=True, add_weights=True,
               overwrite_strange_flavor=True, fix_atmu=False):
    try:
        del rec['event_id']
    except KeyError:
        pass

    if remove_nan:
        print('Delete NaNs...')
        rec.fillna(0, inplace=True)
        mc.fillna(0, inplace=True)
        rec.replace([np.inf, -np.inf], 0, inplace=True)
        mc.replace([np.inf, -np.inf], 0, inplace=True)

    if remove_constant:
        print('Remove constant features...')
        pre_shape = rec.shape
        # constant_feats = rec.loc[:, rec.var() == 0].columns.sort_values()
        rec = rec.copy().loc[:, rec.var() != 0]
        post_shape = rec.shape
        print(pre_shape, ' -> ', post_shape)

    if rescale:
        print('Rescale features...')
        rec = pd.DataFrame(RobustScaler().fit_transform(rec.values),
                           columns=rec.columns)

    if add_flavor:
        print('Generate Flavor...')
        mc = make_flavor(mc)

    if add_target:
        print('Generate Classification target...')
        mc = make_target(mc)
        mc['target_name'] = target_to_name(mc.target)

    if add_weights:
        print('Add weights + fluxes...')
        mc = add_weights_and_fluxes(mc)

    if fix_atmu:
        mc.loc[~mc.is_neutrino, 'wgt_atmo'] = 1/60.0

    return rec, mc
