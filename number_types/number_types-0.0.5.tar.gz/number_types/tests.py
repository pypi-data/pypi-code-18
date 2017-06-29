import os
import sys
import unittest

__dir__ = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, os.path.abspath(os.path.join(__dir__, '..')))

try:
    from number_types import *
finally:
    sys.path.pop(0)


class NumberTypesTest(unittest.TestCase):
    pass
    # TODO

if __name__ == '__main__':
    unittest.main()
