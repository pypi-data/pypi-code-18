from .sha256 import *

if __name__ == "__main__":
    import sys
    print(sha256(bytes.fromhex(sys.argv[1]), int(sys.argv[2])).hex())
