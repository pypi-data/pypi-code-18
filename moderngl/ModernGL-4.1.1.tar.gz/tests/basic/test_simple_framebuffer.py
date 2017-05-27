import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.release()

    def test_framebuffer_color_attachment(self):
        rbo = self.ctx.renderbuffer((64, 64))
        self.ctx.framebuffer(rbo)

    def test_framebuffer_color_attachments(self):
        rbo1 = self.ctx.renderbuffer((64, 64))
        rbo2 = self.ctx.renderbuffer((64, 64))
        rbo3 = self.ctx.renderbuffer((64, 64))
        self.ctx.framebuffer([rbo1, rbo2, rbo3])

    def test_framebuffer_size_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'size'):
            rbo1 = self.ctx.renderbuffer((64, 64))
            rbo2 = self.ctx.depth_renderbuffer((32, 32))
            self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_color_attachments_size_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'size'):
            rbo1 = self.ctx.renderbuffer((64, 64))
            rbo2 = self.ctx.renderbuffer((32, 32))
            self.ctx.framebuffer([rbo1, rbo2])

    def test_depth_framebuffer(self):
        rbo1 = self.ctx.renderbuffer((64, 64))
        rbo2 = self.ctx.depth_renderbuffer((64, 64))
        self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_multisample(self):
        rbo1 = self.ctx.renderbuffer((64, 64), samples=2)
        self.ctx.framebuffer(rbo1)

    def test_depth_framebuffer_multisample(self):
        rbo1 = self.ctx.renderbuffer((64, 64), samples=2)
        rbo2 = self.ctx.depth_renderbuffer((64, 64), samples=2)
        self.ctx.framebuffer(rbo1, rbo2)

    def test_framebuffer_multisample_sample_mismatch(self):
        with self.assertRaisesRegex(ModernGL.Error, 'sample'):
            rbo1 = self.ctx.renderbuffer((64, 64))
            rbo2 = self.ctx.depth_renderbuffer((64, 64), samples=2)
            self.ctx.framebuffer(rbo1, rbo2)

    def test_empty_framebuffer(self):
        with self.assertRaisesRegex(ModernGL.Error, 'empty'):
            self.ctx.framebuffer([])


if __name__ == '__main__':
    unittest.main()
