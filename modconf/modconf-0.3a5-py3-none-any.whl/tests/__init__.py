import unittest
import modconf

class TestFail(unittest.TestCase):
    def test(self):
        try:
            modconf.import_conf('hello')
        except:
            pass


