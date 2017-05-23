import sys
import unittest

from core.run import *
from core.configparser import *
from core.options import *

class InterfaceTests(unittest.TestCase):
    def cli_line(self, *args, **kwargs):
        for arg in args:
            sys.argv.append(arg)
        for k,v in kwargs.items():
            sys.argv.append('--{0}={1}'.format(k,v))
    
    def setUp(self):
        pass
    def tearDown(self):
        sys.argv = sys.argv[1:]
    
    def test_software(self):
        self.assertTrue(True)
        
    def test_config_noexist(self):
        self.cli_line('config', config='/dev/noexist')
        self.assertRaises(FileNotFoundError, loader)
        
    def test_custom_config(self):pass
    
    def test_version(self):
        self.cli_line('-V')
        self.assertRegex(loader(), "^\d+\.\d+\.\d+$")
        
    def test_backup_prep(self): pass
    def test_list(self): pass
    def test_list_prefix(self): pass
    def test_list_empty(self): pass

if __name__ == '__main__':
    unittest.main()