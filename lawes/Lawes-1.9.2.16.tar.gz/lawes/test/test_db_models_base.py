
import unittest
from lawes.test import Fruit

class TestBdModelsBase(unittest.TestCase):

    def setUp(self):
        self.clearall()

    def tearDown(self):
        self.clearall()

    def clearall(self):
        for test_obj in Fruit.objects.filter():
            test_obj.delete()

    def test_delete(self):
        self.clearall()
        for test_obj in Fruit.objects.filter():
            self.fail('delete does not work!')

    # TODO all of them

