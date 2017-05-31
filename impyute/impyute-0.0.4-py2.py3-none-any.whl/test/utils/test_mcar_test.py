"""test_mcar_test.py"""
import unittest
import numpy as np
from impyute.datasets import test_data
from impyute.utils import mcar_test


@unittest.skip('function unfinished')
class TestMCARTest(unittest.TestCase):
    """ Tests for Expectation Maximization"""
    def setUp(self):
        """
        self.data_c: Complete dataset/No missing values
        self.data_m: Incommplete dataset/Has missing values
        """
        mask = np.zeros((5, 5), dtype=bool)
        self.data_c = test_data(mask)
        mask[0][0] = True
        self.data_m = test_data(mask)

    def test_return_type(self):
        """ Check return type, should return a boolean"""
        output = mcar_test(self.data_m)
        self.assertEqual(type(output), type(True))


if __name__ == "__main__":
    unittest.main()
