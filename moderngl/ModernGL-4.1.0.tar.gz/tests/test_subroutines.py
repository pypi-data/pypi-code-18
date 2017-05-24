import struct
import time
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
        if self.ctx.version_code < 400:
            return

        vbo1 = self.ctx.buffer(struct.pack('4f', 0.0, 0.0, 0.0, 0.0))
        vbo2 = self.ctx.buffer(struct.pack('4f', 0.0, 0.0, 0.0, 0.0))

        vert = self.ctx.vertex_shader('''
            #version 400

            in vec4 vert;
            out vec4 color;

            subroutine vec4 color_t();

            subroutine(color_t)
            vec4 ColorRed() {
                return vec4(1, 0, 0, 1);
            }

            subroutine(color_t)
            vec4 ColorBlue() {
                return vec4(0, 0.4, 1, 1);
            }

            subroutine(color_t)
            vec4 ColorYellow() {
                return vec4(1, 1, 0, 1);
            }

            subroutine uniform color_t Color;

            void main() {
                color = vert + Color();
            }
        ''')

        prog = self.ctx.program(vert, ['color'])
        vao = self.ctx.simple_vertex_array(prog, vbo1, ['vert'])

        print(prog.mglo.vertex_shader.subroutines)
        for k, v in prog.mglo.vertex_shader.subroutines.items():
            print(k, v, v.name, v.index)

        print(prog.mglo.vertex_shader.subroutine_uniforms)
        for k, v in prog.mglo.vertex_shader.subroutine_uniforms.items():
            print(k, v, v.name, v.location)

        # print(prog.mglo.vertex_shader.subroutine_locations)

        # prog.mglo.vertex_shader.subroutine_locations = (prog.mglo.vertex_shader.subroutines['ColorYellow'].index,)
        # print(prog.mglo.vertex_shader.subroutine_locations)

        vao.mglo.subroutines = (2,)
        vao.transform(vbo2)
        x, y, z, w = struct.unpack('4f', vbo2.read())
        print(x, y, z, w)

        # prog.mglo.vertex_shader.subroutine_locations = (prog.mglo.vertex_shader.subroutines['ColorBlue'].index,)
        # print(prog.mglo.vertex_shader.subroutine_locations)

        vao.mglo.subroutines = (1,)
        vao.transform(vbo2)
        x, y, z, w = struct.unpack('4f', vbo2.read())
        print(x, y, z, w)

        # prog.mglo.vertex_shader.subroutine_locations = (prog.mglo.vertex_shader.subroutines['ColorRed'].index,)
        # print(prog.mglo.vertex_shader.subroutine_locations)

        vao.mglo.subroutines = (0,)
        vao.transform(vbo2)
        x, y, z, w = struct.unpack('4f', vbo2.read())
        print(x, y, z, w)


if __name__ == '__main__':
    unittest.main()
