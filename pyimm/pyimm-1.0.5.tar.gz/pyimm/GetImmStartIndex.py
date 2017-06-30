'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
from pyimm.immheader import readHeader, isCompressed, offsetToNextHeader

def GetStartPositions(fileName, lastImmIndex):
    with open(fileName, "rb") as f:
        # Get Start Postions
        header = readHeader(f, 0)
        compressed = isCompressed(header)
        if not compressed:
            bytesPerPixel = header['bytes']
            dlen = np.ones(lastImmIndex, dtype='int32') * header['dlen']
            k = np.arange(lastImmIndex,dtype='int64')
            imageStartIndex = 1024L*(k) + dlen*long(bytesPerPixel)*k

        else:
            imageStartIndex = np.zeros(lastImmIndex,dtype='int32')
            thisHeaderOffset = 0
            dlen = np.zeros(lastImmIndex,dtype='int32')
            bytesPerPixel = header['bytes']
            k=0
            imageStartIndex[k] = 0
            dlen[k] = header['dlen']
            for k in range(1,lastImmIndex):
                nextHeaderOffset = offsetToNextHeader(header, thisHeaderOffset)
                header = readHeader(f, offset = nextHeaderOffset)
                dlen[k] = header['dlen']
                thisHeaderOffset = nextHeaderOffset
                imageStartIndex[k] = imageStartIndex[k-1]+1024+dlen[k-1]*(4+bytesPerPixel)
        f.close()
        return imageStartIndex, dlen
