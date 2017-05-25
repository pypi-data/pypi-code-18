# -*- encoding: latin-1 -*-

from __future__ import print_function

import sys

major_version = sys.version_info.major


if major_version >= 3:
    def unicode(text, encoding):
        # TODO: Why is this necessary???
        # On python 2 we need to convert from bytes to unicode, but on python 3 we need the reverse!
        return text.encode("utf-8")


password = u'abcd'
print(password)
print(unicode(password, 'latin-1'))

password = u'abcæøåÆØÅ'
print(password)
print(unicode(password, 'latin-1', errors='ignore'))
