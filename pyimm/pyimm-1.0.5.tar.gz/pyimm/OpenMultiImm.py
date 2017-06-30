'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
import struct

def OpenMultiImm(fileName, firstImage, immCount,imageStartIndex, dlen):
    with open(fileName, "rb") as f:
        # Determine start position of wanted image
        f.seek(108)
        rows = struct.unpack('i', f.read(4))[0]
        f.seek(112)
        cols = struct.unpack('i', f.read(4))[0]
        f.seek(116)
        nbytes = struct.unpack('i', f.read(4))[0]

        f.seek(4)
        compressionFlag = struct.unpack('i', f.read(4))[0]
        if compressionFlag == 6:
            compression = 1
        else:
            compression = 0
        try:
            UCData = np.zeros((immCount, rows*cols),dtype='uint32')
        except  MemoryError as ex: 
            print ("OpenMultiImm: Error Trying to allocate memory " + \
                   str(immCount) + "x" + \
                   str(rows) + "x" + str(cols))
            raise MemoryError(ex)
        if compression == 0:
            for i in range(firstImage,firstImage+immCount):
                immStart = imageStartIndex[i]
                count = dlen[0]
                f.seek(immStart+1024)
                if nbytes == 2:
                    PixelValue = np.fromfile(f, dtype=np.uint16, count = count)
                elif nbytes == 4:
                    PixelValue = np.fromfile(f, dtype=np.uint32, count = count)
                UCData[i-firstImage] = PixelValue            

        else: 
            for i in range(firstImage,firstImage+immCount):
                immStart = imageStartIndex[i]
                PixelNumber = dlen[i]
                f.seek(immStart+1024,0)
                PixelIndex = np.fromfile(f, dtype = np.uint32, count = PixelNumber)+1
                if nbytes == 2:
                    PixelValue = np.fromfile(f, dtype=np.uint16, count = PixelNumber)
                elif nbytes == 4:
                    PixelValue = np.fromfile(f, dtype=np.uint32, count = PixelNumber)
                UCData[i-firstImage][PixelIndex] = PixelValue

        UCData = np.reshape(UCData,(immCount,rows,cols))
        return UCData

def SumMultiImm(fileName, firstImage, immCount,imageStartIndex, dlen):
    with open(fileName, "rb") as f:
        # Determine start position of wanted image
        f.seek(108)
        rows = struct.unpack('i', f.read(4))[0]
        f.seek(112)
        cols = struct.unpack('i', f.read(4))[0]
        f.seek(116)
        nbytes = struct.unpack('i', f.read(4))[0]

        f.seek(4)
        compressionFlag = struct.unpack('i', f.read(4))[0]
        if compressionFlag == 6:
            compression = 1
        else:
            compression = 0
        try:
            UCData = np.zeros((rows*cols),dtype='uint32')
        except  MemoryError as ex: 
            print ("OpenMultiImm: Error Trying to allocate memory " + \
                   str(immCount) + "x" + \
                   str(rows) + "x" + str(cols))
            raise MemoryError(ex)
        if compression == 0:
            for i in range(firstImage,firstImage+immCount):
                immStart = imageStartIndex[i]
                count = dlen[0]
                f.seek(immStart+1024)
                if nbytes == 2:
                    PixelValue = np.fromfile(f, dtype=np.uint16, count = count)
                elif nbytes == 4:
                    PixelValue = np.fromfile(f, dtype=np.uint32, count = count)
                UCData = np.add(UCData, PixelValue/immCount)            

        else: 
            for i in range(firstImage,firstImage+immCount):
                immStart = imageStartIndex[i]
                PixelNumber = dlen[i]
                f.seek(immStart+1024,0)
                PixelIndex = np.fromfile(f, dtype = np.uint32, count = PixelNumber)+1
                if nbytes == 2:
                    PixelValue = np.fromfile(f, dtype=np.uint16, count = PixelNumber)
                elif nbytes == 4:
                    PixelValue = np.fromfile(f, dtype=np.uint32, count = PixelNumber)
                UCData = np.add(UCData, PixelValue/immCount)

        UCData = np.reshape(UCData,(rows,cols))
        print (UCData)
        return UCData
