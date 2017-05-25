import unittest
from lang.builtins import *


class TestDirections(unittest.TestCase):

    def test_min_dir(self):
        self.assertEqual(minDir(), Norte)

    def test_max_dir(self):
        self.assertEqual(maxDir(), Oeste)

    def test_next_dir(self):
        dirs = [Oeste, Norte, Este, Sur, Oeste]
        for i in range(len(dirs) - 1):
            self.assertEqual(siguiente(dirs[i]), dirs[i+1])

    def test_prev_dir(self):
        dirs = [Oeste, Norte, Este, Sur, Oeste]
        for i in range(1, len(dirs)):
            self.assertEqual(previo(dirs[i]), dirs[i-1])

    def test_opposite_dir(self):
        dirs = [Norte, Este, Sur, Oeste]
        opposites = [Sur, Oeste, Norte, Este]
        for i in range(len(dirs)):
            self.assertEqual(opuesto(dirs[i]), opposites[i])


if __name__ == '__main__':
    unittest.main()
