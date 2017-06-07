#!/usr/bin/env python
# vim:set ts=4 sts=4 sw=4 et:

import numpy as np

from sklearn.preprocessing import OneHotEncoder

from km3pipe.mc import pdg2name


def is_nu(flavor):
    nu = np.array(['nu_e', 'anu_e', 'nu_mu', 'anu_mu'])
    return np.in1d(flavor, nu)


def pdg_to_flavor(mc_ids):
    return [pdg2name(int(mc_id)) for mc_id in mc_ids]


def t2f(row):
    return pdg2name(row['type'])


def flavor_col(df):
    return df.apply(t2f, axis=1).astype('str')


class TargetGen():
    """Generate PID targets from MC info.

    Targets are vectors of strings: `['track', 'cscd', ...]`, which can
    be fed to `sklearn.preprocessing.OneHotEncoder` to encode them as
    `[0, 1, ...]`.

    Examples
    --------
    >>> from km3learn.label import TargetGen
    >>> mc_type = mc_info['dusj_MCtype']
    >>> is_cc = np.array([True] * mc_type.shape[0])
    >>> tg = TargetGen(is_cc, mc_type)
    """

    def __init__(self, pdg, is_cc):
        # For any logic operations, use the numpy functions, not pure python
        # Everything should work for both arrays & scalars
        # However, arrays are assumed default
        self.is_cc = np.array(is_cc)
        self.is_nc = np.logical_not(is_cc)
        self.pdg = np.array(pdg)
        self.flavor = pdg_to_flavor(self.pdg)
        self.is_neutrino = is_nu(self.flavor)
        self.is_other = np.logical_not(self.is_neutrino)
        self._n_events = len(self.pdg)

    @property
    def track_cscd_rest(self, rest_val=0, cscd_val=1, track_val=2):
        label = np.full(self._n_events, rest_val, dtype=int)       # rest
        label[self.is_neutrino] = cscd_val        # cscd
        is_mu = np.logical_and(self.is_neutrino,
                               np.abs(self.pdg) == 14)
        is_track = np.logical_and(is_mu, self.is_cc)
        label[is_track] = track_val
        return label


def one_hot(label):
    enc = OneHotEncoder()
    return enc.fit_transform(label)


def target_to_name(labels, classtrans={0: 'background', 1: 'cascade',
                                       2: 'track'}):
    return labels.apply(lambda c: classtrans[c])
