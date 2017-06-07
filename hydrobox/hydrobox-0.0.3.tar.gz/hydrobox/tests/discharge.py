import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
from hydrobox.discharge.stats import flow_duration_curve

# some result container
PROBCALC = np.array([0.04761905, 0.0952381, 0.14285714, 0.19047619, 0.23809524, 0.28571429,  0.33333333,
                     0.38095238, 0.42857143, 0.47619048, 0.52380952, 0.57142857,  0.61904762,  0.66666667,
                     0.71428571, 0.76190476, 0.80952381, 0.85714286, 0.9047619,  0.95238095])

MULTI_PROBCALC = np.array([[0.04761905,  0.04761905,  0.04761905],
                           [0.0952381 ,  0.0952381 ,  0.0952381],
                           [0.14285714, 0.14285714, 0.14285714],
                           [0.19047619, 0.19047619, 0.19047619],
                           [0.23809524, 0.23809524, 0.23809524],
                           [0.28571429, 0.28571429, 0.28571429],
                           [0.33333333, 0.33333333, 0.33333333],
                           [0.38095238, 0.38095238, 0.38095238],
                           [0.42857143, 0.42857143, 0.42857143],
                           [0.47619048, 0.47619048, 0.47619048],
                           [0.52380952, 0.52380952, 0.52380952],
                           [0.57142857, 0.57142857, 0.57142857],
                           [0.61904762, 0.61904762, 0.61904762],
                           [0.66666667, 0.66666667, 0.66666667],
                           [0.71428571, 0.71428571, 0.71428571],
                           [0.76190476, 0.76190476, 0.76190476],
                           [0.80952381, 0.80952381, 0.80952381],
                           [0.85714286, 0.85714286, 0.85714286],
                           [0.9047619, 0.9047619, 0.9047619],
                           [0.95238095, 0.95238095, 0.95238095]]
                          )


class TestFlowDurationCurve(unittest.TestCase):

    def setUp(self):
        """
        Set up some random data.
        :return:
        """
        np.random.seed(42)
        self.gamma = np.random.gamma(2, 2, size=20)
        self.multi_gamma = np.random.gamma(2, 2, size=(20, 3))

    def test_probability_calculation(self):
        assert_array_almost_equal(flow_duration_curve(self.gamma, plot=False), PROBCALC)

    def test_probability_inverse(self):
        assert_array_almost_equal(flow_duration_curve(self.gamma, plot=False, non_exceeding=False), PROBCALC[::-1])

    def test_multi_probablility_calculation(self):
        assert_array_almost_equal(flow_duration_curve(self.multi_gamma, plot=False), MULTI_PROBCALC)

    def test_multi_probability_inverse(self):
        assert_array_almost_equal(
            flow_duration_curve(self.multi_gamma, plot=False, non_exceeding=False),
            MULTI_PROBCALC[::-1]
        )


if __name__ == '__main__':
    unittest.main()
