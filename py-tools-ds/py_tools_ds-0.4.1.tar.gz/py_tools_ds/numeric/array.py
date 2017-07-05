# -*- coding: utf-8 -*-
__author__ = "Daniel Scheffler"

import numpy as np
import warnings



def get_outFillZeroSaturated(dtype):
    """Returns the values for 'fill-', 'zero-' and 'saturated' pixels of an image
    to be written with regard to the target data type.

    :param dtype: data type of the image to be written
    """
    dtype = str(np.dtype(dtype))
    assert dtype in ['int8', 'uint8', 'int16', 'uint16','float32'], \
        "get_outFillZeroSaturated: Unknown dType: '%s'." %dtype
    dict_outFill      = {'int8':-128, 'uint8':0  , 'int16':-9999, 'uint16':9999 , 'float32':-9999.}
    dict_outZero      = {'int8':0   , 'uint8':1  , 'int16':0    , 'uint16':1    , 'float32':0.}
    dict_outSaturated = {'int8':127 , 'uint8':256, 'int16':32767, 'uint16':65535, 'float32':65535.}
    return dict_outFill[dtype], dict_outZero[dtype], dict_outSaturated[dtype]


def find_noDataVal(pathIm_or_GeoArray,bandIdx=0,sz=3):
    """tries to derive no data value from homogenious corner pixels within 3x3 windows (by default)
    :param pathIm_or_GeoArray:
    :param bandIdx:
    :param sz: window size in which corner pixels are analysed
    """
    from geoarray import GeoArray
    geoArr       = pathIm_or_GeoArray if isinstance(pathIm_or_GeoArray, GeoArray) else GeoArray(pathIm_or_GeoArray)
    get_mean_std = lambda corner_subset: {'mean':np.mean(corner_subset), 'std':np.std(corner_subset)}

    wins         = [geoArr[0:sz,0:sz,bandIdx], geoArr[0:sz,-sz:,bandIdx],
                    geoArr[-sz:,-sz:,bandIdx], geoArr[-sz:,0:sz,bandIdx]] # UL, UR, LR, LL
    means_stds   = [get_mean_std(win) for win in wins]

    possVals     = [i['mean'] for i in means_stds if i['std']==0]
    # possVals==[]: all corners are filled with data; np.std(possVals)==0: noDataVal clearly identified

    if possVals:
        if np.std(possVals)!=0:
            # different possible nodata values have been found in the image corner
            return 'ambiguous'
        else:
            if len(possVals)<=2:
                # each window in each corner
                warnings.warn("\nAutomatic nodata value detection returned the value %s for GeoArray '%s' but this "
                              "seems to be unreliable (occurs in only %s). To avoid automatic detection, just pass "
                              "the correct nodata value." %(possVals[0], geoArr.basename,
                                                            ('2 image corners' if len(possVals)==2 else '1 image corner')))
            return possVals[0]
    else:
        return None


