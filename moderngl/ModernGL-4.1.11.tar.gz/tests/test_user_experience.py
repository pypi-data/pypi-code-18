import unittest

import ModernGL


class TestCase(unittest.TestCase):

    def test_1(self):
        self.assertEqual(repr(ModernGL.CORE_330), 'ModernGL.CORE_330')
        self.assertEqual(repr(ModernGL.TRIANGLES), 'ModernGL.TRIANGLES')
        self.assertEqual(repr(ModernGL.BLEND), 'ModernGL.BLEND')


if __name__ == '__main__':
    unittest.main()
