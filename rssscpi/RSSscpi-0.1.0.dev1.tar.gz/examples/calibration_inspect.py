# -*- coding: utf-8 -*-
"""

@author: Lukas Sandström
"""
from __future__ import print_function

from RSSscpi import ZNB

import time, timeit
import sys

from RSSscpi import SocketInterface

import visa

import logging
# logging.basicConfig(level=logging.WARN, filename=__file__[:-3]+"_log.txt", filemode="w")
logging.basicConfig(level=logging.WARN)

# Don't print the traceback of SCPI errors, as the exceptions are asynchronous
def excepthook(type, value, tb):
    if isinstance(value, ZNB.Error) and value.stack:
        sys.stderr.write("ZNB.Error\n")
        sys.stderr.write(str(value))
    else:
        sys.__excepthook__(type, value, tb)
sys.excepthook = excepthook

rm = visa.ResourceManager()

#znb_ip = "10.188.178.47"
znb_ip = "192.168.56.101"
#znb_ip = "10.188.178.63"

visa_res = rm.open_resource('TCPIP::' + znb_ip + '::INSTR')
#visa_res = SocketInterface(znb_ip)
#visa_res = DummyVisa("hej")

# VISA command logging
# Error checking / handling

znb = ZNB(visa_res)

znb.visa_logger.setLevel(logging.DEBUG)
znb.visa_logger.addHandler(logging.FileHandler(filename=__file__[:-3]+"_visa_log.txt", mode="wb"))

znb.init()
znb.RST.w()

# Sense:correction:cdata

ch = znb.get_channel(1)
ch.sweep.points = 3
znb.SENSe(ch.n).FREQuency.STOP().w(4e9)

# print ch.CORRection.DATA.PARameter.COUNt.q()  # funkar med factory cal
# print ch.CORRection.DATA.PARameter.q()  # funkar utan argument
# print ch.CORRection.STATe.q()
# print ch.CORRection.STIMulus.q()

ch.CORRection.COLLect.METHod.DEFine.w("Test", "TRL", (1, 2, 3), fmt="{:q}, {:s}, {:d*}")
ch.CORRection.COLLect.SAVE.SELected.DEFault.w()

# print ch.CORRection.DATE.q()  # funkar ej utan user cal
# for arg in ch.CORRection.DATA.PARameter.args:
#     if arg == "MTESt" or arg == "MVNA":  # only valid for cals with switch matrixes
#         continue
#     print arg, ch.CORRection.DATA.PARameter.q(arg)

freq = ch.CORRection.STIMulus.q()
refl = ch.CORRection.CDATa.q("REFLTRACK", 1, 0, fmt="{:q}, {:d}, {:d}").numpy_complex()
g11 = ch.CORRection.CDATa.q("G11", 1, 2, fmt="{:q}, {:d}, {:d}").numpy_complex()


print(freq, freq.numpy_array()-4e9)
print(refl)
print(g11)

#print ch.CORRection.COLLect.METHod.DEFine.q()

znb.INITiate.CONTinuous().w(False)
znb.INITiate.w()
znb.WAI.w()
znb.query_OPC()
time.sleep(1)
znb.check_error_queue()
print("end")
