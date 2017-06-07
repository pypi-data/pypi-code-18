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

    def test_framebuffer_color_attachment(self):
        rbo = self.ctx.renderbuffer((16, 16))
        self.ctx.framebuffer(rbo)

    def test_framebuffer_color_mask(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)))
        self.assertEqual(fbo.color_mask, (True, True, True, True))

    def test_framebuffer_single_channel_color_mask(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16), components=1))
        self.assertEqual(fbo.color_mask, (True, False, False, False))

    def test_framebuffer_mixed_channels_color_mask(self):
        fbo = self.ctx.framebuffer([
            self.ctx.renderbuffer((16, 16), components=1),
            self.ctx.renderbuffer((16, 16), components=2),
            self.ctx.renderbuffer((16, 16), components=3),
            self.ctx.renderbuffer((16, 16), components=4),
        ])
        mask = (
            (True, False, False, False),
            (True, True, False, False),
            (True, True, True, False),
            (True, True, True, True),
        )
        self.assertEqual(fbo.color_mask, mask)

    def test_framebuffer_depth_mask(self):
        fbo = self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)))
        self.assertEqual(fbo.depth_mask, True)

    def test_framebuffer_color_attachments(self):
        rbo1 = self.ctx.renderbuffer((16, 16))
        rbo2 = self.ctx.renderbuffer((16, 16))
        rbo3 = self.ctx.renderbuffer((16, 16))
        self.ctx.framebuffer([rbo1, rbo2, rbo3])

    def test_framebuffer_multiple_color_masks(self):
        fbo = self.ctx.framebuffer([
            self.ctx.renderbuffer((16, 16)),
            self.ctx.renderbuffer((16, 16)),
        ])
        self.assertEqual(fbo.color_mask, ((True, True, True, True), (True, True, True, True)))

    def test_framebuffer_size_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'size'):
            rbo1 = self.ctx.renderbuffer((16, 16))
            rbo2 = self.ctx.depth_renderbuffer((32, 32))
            self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_color_attachments_size_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'size'):
            rbo1 = self.ctx.renderbuffer((16, 16))
            rbo2 = self.ctx.renderbuffer((32, 32))
            self.ctx.framebuffer([rbo1, rbo2])

    def test_depth_framebuffer(self):
        rbo1 = self.ctx.renderbuffer((16, 16))
        rbo2 = self.ctx.depth_renderbuffer((16, 16))
        self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_multisample(self):
        rbo1 = self.ctx.renderbuffer((16, 16), samples=2)
        self.ctx.framebuffer(rbo1)

    def test_depth_framebuffer_multisample(self):
        rbo1 = self.ctx.renderbuffer((16, 16), samples=2)
        rbo2 = self.ctx.depth_renderbuffer((16, 16), samples=2)
        self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_multisample_sample_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'sample'):
            rbo1 = self.ctx.renderbuffer((16, 16))
            rbo2 = self.ctx.depth_renderbuffer((16, 16), samples=2)
            self.ctx.framebuffer(rbo1, rbo2)

    def test_empty_framebuffer(self):
        with self.assertRaisesRegex(ModernGL.Error, 'empty'):
            self.ctx.framebuffer([])

    def test_framebuffer_having_depth_in_colors(self):
        with self.assertRaisesRegex(ModernGL.Error, r'(color|depth)'):
            self.ctx.framebuffer(self.ctx.depth_renderbuffer((16, 16)))

    def test_framebuffer_having_color_in_depth(self):
        with self.assertRaisesRegex(ModernGL.Error, r'(color|depth)'):
            self.ctx.framebuffer(self.ctx.renderbuffer((16, 16)), self.ctx.renderbuffer((16, 16)))


if __name__ == '__main__':
    unittest.main()
