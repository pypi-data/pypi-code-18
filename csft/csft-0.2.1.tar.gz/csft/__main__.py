#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
The entry point of csft.
"""

import argparse as ap
from os.path import isdir

from . import __name__ as _name
from . import __version__ as _version
from .csft import print_result


def main(argv=None):
    """ Execute the application CLI. """
    parser = ap.ArgumentParser(prog=_name)
    parser.add_argument('-V', '--version', action='version', version=_version)
    parser.add_argument('path', help='the directory to be analyzed')
    args = parser.parse_args(args=argv)
    if not isdir(args.path):
        raise TypeError('%s is not a directory!', args.path)
    return print_result(args.path)


if __name__ == '__main__':
    raise SystemExit(main())
