import unittest

import ModernGL


class TestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(self):
        self.ctx.release()

    def test_vertex_shader(self):

        shader = self.ctx.vertex_shader('''
            #version 330

            void main() {
                gl_Position = vec4(0, 0, 0, 0);
            }
        ''')

    def test_fragment_shader(self):

        shader = self.ctx.fragment_shader('''
            #version 330

            out vec4 color;

            void main() {
                color = vec4(0, 0, 0, 0);
            }
        ''')


if __name__ == '__main__':
    unittest.main()
