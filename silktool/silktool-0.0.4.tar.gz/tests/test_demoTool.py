import unittest
# import mock
import os

from tooler import tool


class DemoToolTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_hello_world(self):
        self.assertEqual(tool.print_hello(), 'Binu Says Hello!!!!')
