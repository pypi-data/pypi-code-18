"""test_dsae.py"""
import unittest
import numpy as np
from impyute.imputations.ts import dsae
from impyute.datasets import test_data
from impyute.utils import config


class TestDSAE(unittest.TestCase):
    """Tests for Denoising Stacked Autoencoder"""
    def setUp(self):
        """
        self.data_c: Complete dataset/No missing values
        self.data_m: Incomplete dataset/Has missing values
        """
        mask = np.zeros((5, 5), dtype=bool)
        self.data_c = test_data(mask)
        self.config = config(self.data_c)
        mask[0][0] = True
        self.data_m = test_data(mask)

    def test_return_type(self):
        """Check return type, should return an np.ndarray"""
        imputed = dsae(self.data_m, self.config)
        self.assertTrue(isinstance(imputed, np.ndarray))
