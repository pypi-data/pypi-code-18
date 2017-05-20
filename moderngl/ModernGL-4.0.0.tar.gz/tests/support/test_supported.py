import importlib
import unittest


class TestCase(unittest.TestCase):

	def test_import_and_context(self):
		ModernGL = importlib.import_module('ModernGL')
		ctx = ModernGL.create_standalone_context()
		ctx.release()


if __name__ == '__main__':
	unittest.main()
