import os.path

import h5py

import km3flux


DATADIR = os.path.dirname(km3flux.__file__) + '/data'
HONDAFILE = DATADIR + '/honda2015_frejus_solarmin.h5'
DM_FILE = DATADIR + '/gc_spectra.h5'
DM_MASSES = {'100000', '260', '100', '5000', '360', '200', '10', '1000', '750',
             '30000', '2000', '50', '10000', '180', '500', '150', '3000', '25',
             '90', '1500'}
DM_FLAVORS = {'anu_mu', 'nu_mu'}
DM_CHANNELS = {'b', 'mu', 'tau', 'w'}


def dm_gc_spectrum(flavor='nu_mu', channel='w', mass='100', full_lims=False):
    """Dark Matter spectra by M. Cirelli."""
    mass = str(mass)
    if mass not in DM_MASSES:
        raise KeyError("Mass '{}' not available.".format(mass))
    if flavor not in DM_FLAVORS:
        raise KeyError("Flavor '{}' not available.".format(flavor))
    if channel not in DM_CHANNELS:
        raise KeyError("Channel '{}' not available.".format(channel))

    fname = DM_FILE
    with h5py.File(fname, 'r') as h5:
        gr = h5[flavor][channel][mass]
        counts = gr['entries'][:]
        bins = gr['binlims'][:]
    if not full_lims:
        bins = bins[:-1]
    return counts, bins
