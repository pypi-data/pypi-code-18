'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''

import unittest
from pyimm.GetImmStartIndex import GetStartPositions
from pyimm.immheader import readHeader
import numpy as np

class Test(unittest.TestCase):


    def setUp(self):
        self.testFileUncompressed = \
            "../testData/" + \
            "A006_PinarFe5wtpPS_7p35keV_20H20V_USID_Sq1_001/" + \
            "A006_PinarFe5wtpPS_7p35keV_20H20V_USID_Sq1_001_00001-00266.imm"
        self.testFileCompressed = \
            "../testData/" + \
            "C035_SilicaNP_022415_0p5vp_GNF15_20H40V_92rows_1ms_FCCDq1_010/" + \
            "C035_SilicaNP_022415_0p5vp_GNF15_20H40V_92rows_1ms_FCCDq1_010_00001-10000.imm"


    def tearDown(self):
        pass


    def testUncompressedGetImmStartPositions(self):
        maxImages = 66
        imageStartIndex, dlen  = \
            GetStartPositions(self.testFileUncompressed,
                             maxImages)
        fp = open(self.testFileUncompressed, "rb")
        header = readHeader(fp, offset=0)
        print header['dlen']
        print header['bytes']
        i = np.array(range(maxImages), dtype='int32')
        realOffset = i * (1024 + header['dlen']*header['bytes'])
        print "realOffset"
        print realOffset
        print "imageStartIndex"
        print imageStartIndex
        print dlen
        for x in range(imageStartIndex.size):
            self.assertEqual(realOffset[x], imageStartIndex[x], 
                         "Check uncompressed offsets")
        for dl in dlen:
            self.assertEqual(header['dlen'], dl, 
                             "checking each uncompressed length")
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()