#!/usr/bin/env python
from PySAIS._sais32 import sais as sais_32
from PySAIS._sais64 import sais as sais_64
from tables.earray import EArray
from tables.array import Array
import numpy as np


def sais(s, reduce_size=True, encoding='ascii'):
    '''
        SAIS wrapper function. Input s should be either bytes, string, numpy
        byte-array or pytables numpy-like array of bytes.

        reduce_size is a flag which controls whether we should convert the
        array to uint16 or uint32 if it makes sense after the suffix array
        is computed.
    '''
    if isinstance(s, bytes):
        pass
    elif isinstance(s, str):
        s = s.encode(encoding)
    elif ((isinstance(s, np.ndarray) or isinstance(s, EArray) or
           isinstance(s, Array)) and isinstance(s[0], np.bytes_)):
        # numpy or pytables numpy-like --> loads to memory
        s = s[:].tobytes()
    else:
        raise ValueError('Pass input as bytes, string, numpy byte-array or '
                         'pytables numpy-like array of bytes.')

    # Compute the suffix array -- the original SAIS code uses 2^30 as a cut-off.
    # Upper limit of 64 bit has (obviously) been untested, but is set at 2^62.
    sa = (sais_32(s) if len(s) < 2**30 else sais_64(s))

    if reduce_size:
        # Reduce the size of the integer type of the *returned* SA if it
        # makes sense.
        if len(sa) <= np.iinfo(np.uint16).max:
            # Converting int32 -> uint16
            sa = sa.astype(np.uint16, copy=False)
        elif (sa.dtype == np.int64) and (len(sa) <= np.iinfo(np.uint32).max):
            # Converting int64 -> uint32.
            sa = sa.astype(np.uint32, copy=False)

    return sa
