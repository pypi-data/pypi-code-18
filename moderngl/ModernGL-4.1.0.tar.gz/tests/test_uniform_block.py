import struct
import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ctx = ModernGL.create_standalone_context()

        self.vert = self.ctx.vertex_shader('''
            #version 330

            in mat2 in_m;
            in vec2 in_v;

            out vec2 out_v;

            uniform Block {
                float x;
            };

            void main() {
                out_v = in_m * in_v * x;
            }
        ''')

        self.prog = self.ctx.program(self.vert, ['out_v'])

    @classmethod
    def tearDownClass(self):
        self.ctx.release()

    def test_1(self):
        buf_m = self.ctx.buffer(struct.pack('4f', 1, 1, 1, 2))
        buf_v = self.ctx.buffer(struct.pack('2f', 4, 7))
        buf_u = self.ctx.buffer(struct.pack('f', 123))
        buf_r = self.ctx.buffer(reserve=buf_v.size)
        res = self.ctx.buffer(reserve=buf_v.size)

        vao = self.ctx.vertex_array(self.prog, [
            (buf_m, '4f', ['in_m']),
            (buf_v, '2f', ['in_v']),
        ])

        self.assertFalse('Block' in self.prog.uniforms)
        self.assertTrue('Block' in self.prog.uniform_blocks)

        buf_u.bind_to_uniform_block(self.prog.uniform_blocks['Block'])

        vao.transform(buf_r, ModernGL.POINTS)
        a, b = struct.unpack('2f', buf_r.read())

        self.assertAlmostEqual(a, 1353.0)
        self.assertAlmostEqual(b, 2214.0)


if __name__ == '__main__':
    unittest.main()
