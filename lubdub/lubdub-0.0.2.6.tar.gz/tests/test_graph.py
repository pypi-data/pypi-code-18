import unittest
import random

from lubdub.exceptions import LubDubError
from lubdub import PlotHRV

from .real_data import HRV_SEQUENCE_4

class TestCalc(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_PlotHRV_empty_data_raises_LubDubError(self):
        with self.assertRaises(LubDubError):
            PlotHRV()

    def test_PlotHRV_with_too_short_RRS_returns_empty(self):
        rrs = [972.0, 1089.0, 1257.0, 1214.0, 1054.0, 1164.0, 1312.0, 1261.0, 1121.0]
        result = PlotHRV(rrs)
        assert result['y_values'] == []
        assert result['y_range'] == ()


