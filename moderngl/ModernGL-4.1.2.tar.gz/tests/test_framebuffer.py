import struct
import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(self):
        self.ctx.release()

    def test_1(self):
        size = (4, 4)
        rbo1 = self.ctx.renderbuffer(size, floats=False)
        rbo2 = self.ctx.renderbuffer(size)
        rbo3 = self.ctx.renderbuffer(size)
        fbo1 = self.ctx.framebuffer(rbo1)
        fbo2 = self.ctx.framebuffer(rbo2)
        fbo3 = self.ctx.framebuffer(rbo3)
        fbo4 = self.ctx.framebuffer([rbo1, rbo2, rbo3])

        fbo4.clear(0.0, 0.6, 0.7, 1.0)

        pixels1 = fbo1.read(components=4, floats=False)
        self.assertEqual(pixels1, b'\x00\x99\xb2\xff' * 16)

        pixels2 = fbo1.read(components=4, floats=False)
        self.assertEqual(pixels2, b'\x00\x99\xb2\xff' * 16)

        pixels3 = fbo1.read(components=4, floats=False)
        self.assertEqual(pixels3, b'\x00\x99\xb2\xff' * 16)

    def test_2(self):
        size = (4, 4)
        rbo1 = self.ctx.renderbuffer(size, floats=False)
        rbo2 = self.ctx.renderbuffer(size)
        rbo3 = self.ctx.renderbuffer(size)
        fbo1 = self.ctx.framebuffer(rbo1)
        fbo2 = self.ctx.framebuffer(rbo2)
        fbo3 = self.ctx.framebuffer(rbo3)
        fbo4 = self.ctx.framebuffer([rbo1, rbo2, rbo3])

        fbo1.clear(1.0, 0.0, 0.0, 1.0)
        fbo2.clear(0.0, 1.0, 0.0, 1.0)
        fbo3.clear(0.0, 0.0, 1.0, 1.0)

        pixels1 = fbo4.read(attachment=0, components=4, floats=False)
        self.assertEqual(pixels1, b'\xff\x00\x00\xff' * 16)

        pixels2 = fbo4.read(attachment=1, components=4, floats=False)
        self.assertEqual(pixels2, b'\x00\xff\x00\xff' * 16)

        pixels3 = fbo4.read(attachment=2, components=4, floats=False)
        self.assertEqual(pixels3, b'\x00\x00\xff\xff' * 16)


if __name__ == '__main__':
    unittest.main()
