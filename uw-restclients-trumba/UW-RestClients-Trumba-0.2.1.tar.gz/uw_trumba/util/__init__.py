import sys


def to_bytestring(string):
    if (sys.version_info > (3, 0)):
        return string.encode()
    else:
        return bytes(string)
