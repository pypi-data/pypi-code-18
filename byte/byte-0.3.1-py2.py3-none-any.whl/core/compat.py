"""byte - compatibility module."""
from __future__ import absolute_import, division, print_function

import sys

PY2 = sys.version_info[0] == 2
PY26 = sys.version_info[0:2] == (2, 6)
PY27 = sys.version_info[0:2] == (2, 7)

PY3 = sys.version_info[0] == 3
PY34 = sys.version_info[0:2] == (3, 4)

PYPY = hasattr(sys, 'pypy_translation_info')
PYPY2 = PYPY and PY27
PYPY3 = PYPY and PY3
