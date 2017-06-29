#!/usr/bin/env python3

import sys

from .utils import args
from .Stops import Stops


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "stops" or sys.argv[1] == "-s":
            a = args(sys.argv, ["/stoptimes/", "/merged/stops/"])
            s = Stops(a[0], a[1])
            s.write()
    else:
        a = args(sys.argv)


if __name__ == "__main__":
    main()
