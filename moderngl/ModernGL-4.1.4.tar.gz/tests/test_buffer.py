import unittest

import ModernGL


class TestBuffer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = ModernGL.create_standalone_context()

    @classmethod
    def tearDownClass(cls):
        cls.ctx.release()

    def tearDown(self):
        self.assertEqual(self.ctx.error, 'GL_NO_ERROR')

    def test_buffer_clear_1(self):
        buf = self.ctx.buffer(data=b'\xAA\x55' * 10)
        buf.clear(chunk=b'AB')
        self.assertEqual(buf.read(), b'AB' * 10)

    def test_buffer_clear_2(self):
        buf = self.ctx.buffer(data=b'\xAA\x55' * 10)
        buf.clear(offset=1, size=18, chunk=b'AB')
        self.assertEqual(buf.read(), b'\xAAABABABABABABABABAB\x55')

    def test_buffer_create(self):
        buf = self.ctx.buffer(data=b'\xAA\x55' * 10)
        self.assertEqual(buf.read(), b'\xAA\x55' * 10)

    def test_buffer_read_write(self):
        buf = self.ctx.buffer(reserve=10)
        buf.write(b'abcd')
        self.assertEqual(buf.read(4), b'abcd')
        buf.write(b'abcd', offset=3)
        self.assertEqual(buf.read(4, offset=1), b'bcab')
        buf.write(b'abcd', offset=6)
        self.assertEqual(buf.read(), b'abcabcabcd')
        self.assertEqual(buf.read(offset=3), b'abcabcd')

    def test_buffer_read_into(self):
        data = b'Hello World!'
        buf = self.ctx.buffer(data)
        res = bytearray(buf.size)
        buf.read_into(res)
        self.assertEqual(data, bytes(res))

    def test_buffer_access_read_into(self):
        data = b'Hello World!'
        buf = self.ctx.buffer(data)
        res = bytearray(buf.size)

        with buf.access() as access:
            access.read_into(res)

        self.assertEqual(data, bytes(res))

    def test_buffer_orphan(self):
        buf = self.ctx.buffer(reserve=1024)
        buf.orphan()

    def test_buffer_invalidate(self):
        buf = self.ctx.buffer(reserve=1024)
        buf.release()

        self.assertEqual(type(buf), ModernGL.InvalidObject)

        with self.assertRaises(AttributeError):
            buf.read()

    def test_buffer_access(self):
        buf = self.ctx.buffer(data=b'\xAA\x55' * 10)

        with buf.access() as a:
            self.assertEqual(a.read(), b'\xAA\x55' * 10)

    def test_buffer_reentrant_access(self):
        buf = self.ctx.buffer(reserve=1024)

        with buf.access():
            with self.assertRaises(ModernGL.Error):
                buf.read()

        self.assertNotEqual(self.ctx.error, 'GL_NO_ERROR')


if __name__ == '__main__':
    unittest.main()
