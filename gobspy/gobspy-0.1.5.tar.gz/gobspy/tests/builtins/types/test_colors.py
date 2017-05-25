import unittest
from lang.builtins import *


class TestColors(unittest.TestCase):

    def test_min_color(self):
        self.assertEqual(minColor(), Azul)

    def test_max_color(self):
        self.assertEqual(maxColor(), Verde)

    def test_next_color(self):
        colors = [Verde, Azul, Negro, Rojo, Verde]
        for i in range(len(colors) - 1):
            self.assertEqual(siguiente(colors[i]), colors[i+1])

    def test_prev_color(self):
        colors = [Verde, Azul, Negro, Rojo, Verde]
        for i in range(1, len(colors)):
            self.assertEqual(previo(colors[i]), colors[i-1])

    def test_opposite_color(self):
        colors = [Azul, Negro, Rojo, Verde]
        opposites = [Rojo, Verde, Azul, Negro]
        for i in range(len(colors)):
            self.assertEqual(opuesto(colors[i]), opposites[i])


if __name__ == '__main__':
    unittest.main()
