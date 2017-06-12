import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.release()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_texture(self):
        self.ctx.texture((16, 16), 3)

    def test_multisample_texture(self):
        self.ctx.texture((16, 16), 3, samples=2)

    def test_depth_texture(self):
        self.ctx.depth_texture((16, 16))

    def test_multisample_depth_texture(self):
        self.ctx.depth_texture((16, 16), samples=2)

    def test_texture_invalid_samples(self):
        with self.assertRaisesRegex(ModernGL.Error, 'sample'):
            self.ctx.texture((16, 16), 3, samples=3)

    def test_texture_get_swizzle(self):
        tex = self.ctx.texture((16, 16), 4)
        self.assertEqual(tex.swizzle, 'RGBA')

    def test_texture_swizzle_1(self):
        tex = self.ctx.texture((16, 16), 4)
        tex.swizzle = 'argb'
        self.assertEqual(tex.swizzle, 'ARGB')

    def test_texture_swizzle_2(self):
        tex = self.ctx.texture((16, 16), 1)
        tex.swizzle = 'RRRR'
        self.assertEqual(tex.swizzle, 'RRRR')

    def test_texture_swizzle_3(self):
        tex = self.ctx.texture((16, 16), 2)
        tex.swizzle = '01RG'
        self.assertEqual(tex.swizzle, '01RG')


if __name__ == '__main__':
    unittest.main()
