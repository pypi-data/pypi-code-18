#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
The entry point of csft.
"""

import argparse as ap
from os.path import isdir

from .csft import print_result


def main(argv=None):
    parser = ap.ArgumentParser(add_help='add help')
    parser.add_argument('path', help='the directory to be analyzed')
    args = parser.parse_args(args=argv)
    if not isdir(args.path):
        raise TypeError('%s is not a directory!', args.path)
    return print_result(args.path)


if __name__ == '__main__':
    raise SystemExit(main())
