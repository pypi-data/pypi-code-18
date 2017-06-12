import sys
import unittest

from sheepcore.run import *
from sheepcore.parser import *
from sheepcore.options import *

class ApiTests(unittest.TestCase):
    def cli_line(self, *args, **kwargs):
        for arg in args:
            sys.argv.append(arg)
        for k,v in kwargs.items():
            sys.argv.append('--{0}={1}'.format(k,v))
            
    def loader_option(self, opt):
        # Get loaded config
        return loader(testopt=opt)
    
    def setUp(self):
        sys.argv = ['dummyscript.py']
        #sys.argv.append('--config=whatever.yaml')
    
    def tearDown(self):
        sys.argv = sys.argv[1:]
    
    

if __name__ == '__main__':
    unittest.main()