#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
The entry point of csft.
"""

import argparse as ap
from pathlib import Path

from . import __name__ as _name
from . import __version__ as _version
from .csft import csft2data, Column


def _dir(path_str):
    path = Path(path_str)
    if not path.is_dir():
        raise TypeError('%s is not a directory!', path_str)
    else:
        return path


def _positive_int(num):
    number = int(num)
    if number <= 0:
        raise ValueError('%s is not positive!', number)
    return number


def _parse_args(argv):
    parser = ap.ArgumentParser(prog=_name)
    parser.add_argument('-V', '--version', action='version', version=_version)
    parser.add_argument('path', type=_dir, help='the directory to be analyzed')
    parser.add_argument('--top', type=_positive_int, metavar='N',
                        help='only display top N results')
    parser.add_argument('-p', '--pretty', action='store_true',
                        help='print size with units')

    return parser.parse_args(args=argv)


def pretty_byte(byte):
    """
    Convert raw bytes to a value with an appropriate unit.

    :param byte: The number of bytes to be convert.
    :return: A value with an appropriate unit.
    """
    if byte < 0:
        raise ValueError('%s is not positive!', byte)

    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']
    index = 0
    for index, _ in enumerate(units):
        if byte >> (10 * (index + 1)) <= 0:
            break
    return '%d %s' % (byte / (1024 ** index), units[index])


def main(argv=None):
    """Execute the application from CLI."""
    args = _parse_args(argv)
    data = csft2data(args.path)

    if args.top:
        data = data.head(args.top)

    if args.pretty:
        data[Column.SIZE] = data[Column.SIZE].map(pretty_byte)

    print(data)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
