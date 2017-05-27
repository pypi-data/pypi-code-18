import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.release()

    def test_texture(self):
        self.ctx.texture((64, 64), 3)

    def test_multisample_texture(self):
        self.ctx.texture((64, 64), 3, samples=2)

    def test_depth_texture(self):
        self.ctx.depth_texture((64, 64))

    def test_multisample_depth_texture(self):
        self.ctx.depth_texture((64, 64), samples=2)

    def test_texture_invalid_samples(self):
        with self.assertRaisesRegex(ModernGL.Error, 'sample'):
            self.ctx.texture((64, 64), 3, samples=3)


if __name__ == '__main__':
    unittest.main()
