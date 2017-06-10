"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -ms3manage` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``s3manage.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``s3manage.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
from __future__ import print_function

import argparse
import sys

from s3manage.buckets import Buckets
from s3manage.index import Index

parser = argparse.ArgumentParser(description='Command description.')
parser.add_argument('buckets', metavar='NAME', nargs=argparse.ONE_OR_MORE,
                    help="The bucket to add indexes to")
parser.add_argument('--include-indexes', action='store_true',
                    help="Include the index files in the generated files")
parser.add_argument('--base-path', '-b', metavar='PATH', action='store',
                    default='',
                    help="Only generate index files under the specified path")


def indexes(args=None):
    args = parser.parse_args(args=args)
    print("Connecting to S3")
    buckets = Buckets()
    print("Verifying buckets")
    valid, invalid = buckets.validate_buckets(args.buckets)
    # Buckets we cannot find indicate a problem
    if invalid:
        print("Missing buckets: ")
        [print("    {0}".format(name)) for name in invalid]
        sys.exit(1)
    for bucket in valid:
        index = Index(bucket)
        print("Constructing index for {0}".format(bucket.get_name()))
        index.construct()
        index.write_indexes()
