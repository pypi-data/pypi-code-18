# -*- coding:utf-8 -*-

import binascii


def MyAHex( str):
    return binascii.a2b_hex(str.replace(' ',''))

def MyHexA( str):
    return binascii.b2a_hex(str).upper()

def dataProcess( str):
    return binascii.a2b_hex(str.replace(' ',''))[10:]

def xor( data):
    lrc = int(0)
    for c in data:
        lrc = lrc ^ c
    return self.MyAHex("%02x" % lrc)

def SeriportPack( sdata):
    sdata = b"\x02" + self.MyAHex("%08x"%(len(sdata))) + sdata
    lrc = self.xor(sdata)
    result=sdata+lrc + b"\x03"
    return result
