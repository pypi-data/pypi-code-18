import sys
import unittest

from sheepcore.run import *
from sheepcore.parser import *
from sheepcore.options import *
from sheepcore.exceptions import *

try:
    TEST_API_KEY = os.environ['TEST_API_KEY']
except:
    print('Pass in TEST_API_KEY env var to run tests')
    sys.exit()

class InterfaceTests(unittest.TestCase):
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
    
    def test_software(self):
        self.assertTrue(True)
        
    def test_config_noexist(self):
        self.cli_line('config', config='/dev/noexist')
        self.assertRaises(RuntimeError, loader)
        
    def test_custom_config(self):pass
    
    def test_version(self):
        self.cli_line('-V')
        self.assertRegex(loader(), "^\d+\.\d+\.\d+$")
        
    def test_backup_prep(self): pass

    def test_invalid_config(self):
        # we have an invalid config passed (since ~/.sheepbackups/config.yaml probably wont exist)
        cfg = self.loader_option('config')
        opts = self.loader_option('opts')
        
        self.assertTrue('example' in cfg['backups'])
        
        with self.assertRaises(SheepAPIError): # With no config key loaded, should fail
            res = run_ping(raw=True)
            
    def test_valid_config(self):
        create config file
        self.cli_line('config', 'myconfig.yaml')
        pass

    def test_list(self): 
        self.cli_line('list')
        self.assertTrue(loader())
        
    def test_list_prefix(self): pass
    def test_list_empty(self): pass

if __name__ == '__main__':
    unittest.main()