import importlib
import unittest


class TestCase(unittest.TestCase):

    def test_import_and_context(self):
        mgl = importlib.import_module('ModernGL')
        ctx = mgl.create_standalone_context(require=mgl.CORE_330)
        ctx.release()


if __name__ == '__main__':
    unittest.main()
