from unittest import TestCase

from keras import applications

from netception.inceptor import Inceptor


class TestInceptor(TestCase):
    _model = None

    @classmethod
    def setUpClass(cls):
        cls._model = applications.VGG16()

    @classmethod
    def tearDownClass(cls):
        del cls._model

    def test_incept_max_steps(self):
        model = self._model
        target = model.get_layer("block5_conv3").output[:, :, :, 455]
        inceptor = Inceptor(model, target, max_steps=2)
        inception, score = inceptor.incept()
        self.assertTupleEqual((None, *inception.shape), model.input_shape)
        self.assertTrue(score > 0.0)

    def test_incept_early_stopping(self):
        model = self._model
        target = model.get_layer("block5_conv3").output[:, :, :, 455]
        inceptor = Inceptor(model, target, max_steps=20,
                            improvement_check_interval=1,
                            improvement_threshold=0.5)
        inception, score = inceptor.incept()
        self.assertTupleEqual((None, *inception.shape), model.input_shape)
        self.assertTrue(score > 0.0)

    def test_incept_invalid_max_steps(self):
        with self.assertRaises(ValueError):
            Inceptor(None, None, max_steps=0)

    def test_incept_invalid_inception_rate(self):
        with self.assertRaises(ValueError):
            Inceptor(None, None, inception_rate=0.0)

    def test_incept_invalid_improvement_check_interval(self):
        with self.assertRaises(ValueError):
            Inceptor(None, None, improvement_check_interval=0)

    def test_incept_invalid_improvement_threshold_low(self):
        with self.assertRaises(ValueError):
            Inceptor(None, None, improvement_threshold=-0.01)

    def test_incept_invalid_improvement_threshold_high(self):
        with self.assertRaises(ValueError):
            Inceptor(None, None, improvement_threshold=1.01)
