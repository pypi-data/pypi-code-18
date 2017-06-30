'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''

import unittest
from pyimm.immheader import readHeader, offsetToNextHeader

class Test(unittest.TestCase):


    def setUp(self):
        self.testFile = "../testData/A006_PinarFe5wtpPS_7p35keV_20H20V_USID_Sq1_001/A006_PinarFe5wtpPS_7p35keV_20H20V_USID_Sq1_001_00001-00266.imm"
        self.testFile2 = "../testData/C035_SilicaNP_022415_0p5vp_GNF15_20H40V_92rows_1ms_FCCDq1_010/C035_SilicaNP_022415_0p5vp_GNF15_20H40V_92rows_1ms_FCCDq1_010_00001-10000.imm"

    def tearDown(self):
        pass


    def testFirstHeaderUncompressed(self):
        fp = open(self.testFile, "rb")        
        header = readHeader(fp, offset=0)
        self.assertEqual(1340, header['cols'], 'Number of Columns check')
        self.assertEqual(1300, header['rows'], 'Number of Rows check')
        print header

    def testFirstHeaderCompressed(self):
        fp = open(self.testFile2, "rb")        
        header = readHeader(fp, offset=0)
        self.assertEqual(960, header['cols'], 'Number of Columns check')
        self.assertEqual(92, header['rows'], 'Number of Rows check')
        print header
        
        

    def testOffsetToNextHeaderUncompressed(self):
        fp = open(self.testFile, "rb")        
        header = readHeader(fp, offset=0)
        self.assertEqual(1340, header['cols'], 'Number of Columns check')
        self.assertEqual(1300, header['rows'], 'Number of Rows check')
        thisOffset = 0
        nextOffset = offsetToNextHeader(header, 0)
        numImages = 1
        while header <> 'eof':
            header = readHeader(fp, offset=nextOffset)
            if header <> 'eof':
                self.assertEqual(1340, header['cols'], 'Number of Columns check')
                self.assertEqual(1300, header['rows'], 'Number of Rows check')
                thisOffset = nextOffset
                nextOffset = offsetToNextHeader(header, thisOffset)
                numImages += 1
            
        self.assertEqual(266, numImages, 'Number of images wrong')
        
    def testOffsetToNextHeaderCompressed(self):
        fp = open(self.testFile2, "rb")        
        header = readHeader(fp, offset=0)
        self.assertEqual(960, header['cols'], 'Number of Columns check')
        self.assertEqual(92, header['rows'], 'Number of Rows check')
        thisOffset = 0
        nextOffset = offsetToNextHeader(header, 0)
        numImages = 1
        while header <> 'eof':
            header = readHeader(fp, offset=nextOffset)
            if header <> 'eof':
                self.assertEqual(960, header['cols'], 'Number of Columns check')
                self.assertEqual(92, header['rows'], 'Number of Rows check')
                thisOffset = nextOffset
                nextOffset = offsetToNextHeader(header, thisOffset)
                numImages += 1
            
        self.assertEqual(10000, numImages, 'Number of images wrong')
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()