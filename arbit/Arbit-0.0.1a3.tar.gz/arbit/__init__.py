from __future__ import absolute_import, division, print_function, unicode_literals
from . import sha256
import sys

if __name__ == "__main__":
    print(sha256(bytes.fromhex(sys.argv[1]), int(sys.argv[2])).hex())
