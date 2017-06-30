'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''
import struct

HEADER_SIZE_IN_BYTES = 1024

## Code for setting up the IMM header was taken from some dev code 
#  Written By Tim Madden APS/XSD-DET.  Many thanks for working out these 
#  details.
imm_headformat = "ii32s16si16siiiiiiiiiiiiiddiiIiiI40sf40sf40sf40sf40sf40sf40sf40sf40sf40sfffiiifc295s84s12s"

imm_fieldnames = [
'mode',
'compression',
'date',
'prefix',
'number',
'suffix',
'monitor',
'shutter',
'row_beg',
'row_end',
'col_beg',
'col_end',
'row_bin',
'col_bin',
'rows',
'cols',
'bytes',
'kinetics',
'kinwinsize',
'elapsed',
'preset',
'topup',
'inject',
'dlen',
'roi_number',
'buffer_number',
'systick',
'pv1',
'pv1VAL',
'pv2',
'pv2VAL',
'pv3',
'pv3VAL',
'pv4',
'pv4VAL',
'pv5',
'pv5VAL',
'pv6',
'pv6VAL',
'pv7',
'pv7VAL',
'pv8',
'pv8VAL',
'pv9',
'pv9VAL',
'pv10',
'pv10VAL',
'imageserver',
'CPUspeed',
'immversion',
'corecotick',
'cameratype',
'threshhold',
'byte632',
'empty_space',
'ZZZZ',
'FFFF'

]

def readHeader(fp, offset=0):
    fp.seek(offset)
    bindata = fp.read(1024)
    if bindata == '':
        return('eof')

    imm_headerdat = struct.unpack(imm_headformat,bindata)
    imm_header ={}
    for k in range(len(imm_headerdat)):
        imm_header[imm_fieldnames[k]]=imm_headerdat[k]
    return(imm_header)

def offsetToNextHeader(header, offsetToThisHeader):
    offset = -1
    compressed = isCompressed(header)
    
    bytesPerPixel = header['bytes']
    dataLength = header['dlen']
    if not compressed:
        offset = offsetToThisHeader + 1024L + dataLength*long(bytesPerPixel)
    else:
        offset = offsetToThisHeader + 1024L + dataLength*(4+long(bytesPerPixel))
    return offset

def readAllHeaders(fp, numImages ):
    offsetToNext = 0
    h = {}
    for i in range(numImages):
        offsetToThisHeader = offsetToNext
        h[i] = readHeader(fp, offsetToThisHeader)
        offsetToNext = offsetToNextHeader(h[i], offsetToThisHeader)
    return h

def verifyImageOrder(fp, headerItem):
    '''
    verify image order in this file.  This is done by looking at one of the 
    items in the headers (i.e. systick, corecotick) which are assumed to 
    increment by one for each image in the file
    '''
    numImages = getNumberOfImages(fp)
    print("verifyImageOrder: numImages = %d" % numImages)
    headers = readAllHeaders(fp, numImages)
    lastImage = -999999
    count = 0
    for head in headers.keys():
        if head > 0:              # first image is assumed in order
            thisImage =  headers[head][headerItem]
            if thisImage != (lastImage + 1):
                count += 1
                print ("verifyImageOrder Image %d out of order, count %d" % 
                       (head,count) )
            #set lastImage = thisImage for next time through
            lastImage = thisImage
        else:
            # record first image as last image
            lastImage =  headers[head][headerItem]


def isCompressed(header):
    if header['compression'] == 6:
        return True
    else:
        return False
    
def getNumberOfImages(fp):
    header = readHeader(fp, offset=0)
    numImages = 1
    
    offsetToNext = offsetToNextHeader(header, 0)
    header = readHeader(fp, offset=offsetToNext)
    while header != 'eof':
        offsetToThisHeader = offsetToNext
        numImages += 1
        offsetToNext = \
            offsetToNextHeader(header, offsetToThisHeader)
        header = readHeader(fp, offset=offsetToNext)
    return numImages
