import unittest
import numpy as np

from somber.utils import expo, linear, resize, np_min, np_max


class TestUtils(unittest.TestCase):

    def test_resize(self):

        X = np.arange(200).reshape(20, 10)
        X_shape = resize(X, (10, 2, 10))
        X_shape_np = np.resize(X, (10, 2, 10))
        self.assertTrue(np.all(X_shape == X_shape_np))

    def test_min(self):

        X = np.array([[1, 2, 3, 4, 5], [6, 0, 6, 8, 0]])
        min_val = np_min(X)
        min_ax0, argmin_ax0 = np_min(X, 0)
        min_ax1, argmin_ax1 = np_min(X, 1)

        self.assertEquals(min_val, 0)
        self.assertTrue(np.all(min_ax0 == X[argmin_ax0, np.arange(5)]))
        self.assertTrue(np.all(min_ax1 == X[np.arange(2), argmin_ax1]))

    def test_max(self):

        X = np.array([[1, 2, 3, 4, 5], [6, 0, 6, 8, 0]])
        min_val = np_max(X)
        min_ax0, argmax_ax0 = np_max(X, 0)
        min_ax1, argmax_ax1 = np_max(X, 1)

        self.assertEquals(min_val, 8)
        self.assertTrue(np.all(min_ax0 == X[argmax_ax0, np.arange(5)]))
        self.assertTrue(np.all(min_ax1 == X[np.arange(2), argmax_ax1]))

    def test_expo_test(self):

        X = 10
        total_steps = 10
        prev = X

        for x in range(total_steps):
            prev_n = expo(X, x, total_steps)
            if x != 0:
                self.assertTrue(np.isclose(prev_n / prev, .77880079))
            prev = prev_n
        self.assertTrue(np.isclose(prev, 1.05399))

    def test_linear_test(self):

        X = 10
        total_steps = 100

        for x in range(total_steps):
            prev = linear(X, x, total_steps)
            self.assertAlmostEqual(prev / X, (1 - (x / total_steps)) + 0.001)

if __name__ == "__main__":
    unittest.main()
