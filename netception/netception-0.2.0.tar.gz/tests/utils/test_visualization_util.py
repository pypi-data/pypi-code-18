from unittest import TestCase

import numpy

from netception.utils.visualization_util import VisualizationUtil


class TestVisualizationUtil(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inception_shape = (32, 32, 3)
        cls.inception = numpy.random.random(cls.inception_shape) - 0.5

    def test_inception_to_bytes(self):
        image_bytes = VisualizationUtil.inception_to_bytes(self.inception)
        self.assertTupleEqual(image_bytes.shape, self.inception_shape)
        self.assertTrue(image_bytes.dtype == numpy.uint8)

    def test_invalid_colorfulness_low(self):
        with self.assertRaises(ValueError):
            VisualizationUtil.inception_to_bytes(
                self.inception, colorfulness=-0.01)

    def test_invalid_colorfulness_high(self):
        with self.assertRaises(ValueError):
            VisualizationUtil.inception_to_bytes(
                self.inception, colorfulness=1.01)

    def test_invalid_inception(self):
        with self.assertRaises(ValueError):
            VisualizationUtil.inception_to_bytes(self.inception.tolist())
