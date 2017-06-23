import unittest
import modconf

class TestClass(unittest.TestCase):
    def test(self):
        cls = modconf.import_class('modconf.tests.conf.conf_class', 'Conf', ('hello', 1))
        print(cls)

