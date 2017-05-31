# -*- coding: utf-8 -*-
"""
    onyx_babel
"""
import sys


PY2 = sys.version_info[0] == 2


if PY2:
    text_type = unicode
    string_types = (str, unicode)
else:
    text_type = str
    string_types = (str, )
