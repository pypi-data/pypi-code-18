#!/usr/bin/env python3

import argparse
import os
import sys

from datetime import datetime
from io import StringIO
from os.path import (
    exists,
    join,
)


def main():
    parser = argparse.ArgumentParser(
        description='Dump mails into files. Can be used as a '
                    'replacement for sendmail or an SMTP server'
    )
    parser.add_argument(
        '--dir',
        default='.',
        help='Directory in which to save the mails.',
    )
    args = parser.parse_args()
    read(args)


def read(args):
    content = StringIO()
    for line in iter(sys.stdin.readline, ''):
        content.write(line)

    save(content, folder=args.dir)


def save(content, folder='.'):
    try:
        os.makedirs(folder, exist_ok=True)
    except FileExistsError:
        print('{} is a file'.format(folder), file=sys.stderr)
    else:
        file_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S.mbox')
        file_path = join(folder, file_name)
        with open(file_path, 'w') as output:
            output.write(content.getvalue())


if __name__ == '__main__':
    main()
