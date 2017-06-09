import os, traceback, logging, lxml.etree

from cppa3.cppa23 import cpp23, cpa23

import unittest

from inspect import getsourcefile
from os.path import abspath, dirname, join

class CPPA23TestCase( unittest.TestCase ):

    def setUp(self):
        logging.getLogger('').handlers = []
        logging.basicConfig(level=logging.DEBUG,
                            filename="cppa23_test.log")
        thisdir = dirname(abspath(getsourcefile(lambda:0)))
        self.testdatadir = join(thisdir,'data23')
        self.parser = lxml.etree.XMLParser(remove_blank_text=True)

    def upconvert_cpp(self, id):
        logging.info('------------------------------------------')
        logging.info('Running test {}'.format(id))
        cppa23(id)

    def upconvert_cpa(self, id):
        logging.info('------------------------------------------')
        logging.info('Running test {}'.format(id))

        cppa2_file = os.path.join(self.testdatadir,'cpa2_'+id+'.xml')
        cppa3_file = os.path.join(self.testdatadir,'cpa3_'+id+'.xml')
        inputdoc =  (lxml.etree.parse(cppa2_file, self.parser)).getroot()
        outputdoc = cpa23(inputdoc)
        fd = open(cppa3_file, 'wb')
        fd.write(lxml.etree.tostring(outputdoc, pretty_print=True))
        fd.close()

    def test_0001(self):
        self.upconvert_cpa('0001')


