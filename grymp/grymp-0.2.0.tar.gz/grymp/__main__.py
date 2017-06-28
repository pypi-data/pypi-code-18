#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import os
import sys
import argparse
import logging

import grymp
from grymp import util, transferer
from grymp.processors import extras, feature

logger = logging.getLogger(__name__)


def _parse_args(args):
    """
    Interpret command line arguments.

    :param args: `sys.argv`
    :return: The populated argparse namespace.
    """

    parser = argparse.ArgumentParser(prog='grymp',
                                     description='Automate the processing of '
                                                 'Grym/vonRicht releases')
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s ' + grymp.__version__)
    parser.add_argument('-v', '--verbosity',
                        help='increase output verbosity',
                        action='count',
                        default=0)
    parser.add_argument('-i', '--interactive',
                        help='prompt before each operation affecting the '
                             'filesystem',
                        action='store_true')
    parser.add_argument('-o', '--overwrite',
                        help='overwrite files without asking',
                        action='store_true')
    parser.add_argument('-k', '--keep',
                        help='keep original files and directory structure; '
                             'note this does not affect files that were moved '
                             'because the destination was on the same '
                             'filesystem, and will only remove the root '
                             'directory if both the feature and extras were '
                             'processed (`-f` and `-e` passed)',
                        action='store_true')
    parser.add_argument('-f', '--feature',
                        help='marshal the feature into this directory (it must '
                             'exist)')
    parser.add_argument('-e', '--extras',
                        help='marshal the extras into a new subdirectory '
                             'within this directory, named after the feature')
    parser.add_argument('base',
                        help='one or more root directories of releases, '
                             'each containing a feature',
                        nargs='+',
                        type=util.decode_cli_arg)
    return parser.parse_args(args[1:])


def main(args):
    """
    grymp's entry point.

    :param args: Command-line arguments, with the program in position 0.
    """

    args = _parse_args(args)

    # sort out logging output and level
    level = util.log_level_from_vebosity(args.verbosity)
    root = logging.getLogger()
    root.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    root.addHandler(handler)

    logger.debug(args)

    if not args.feature and not args.extras:
        util.print_error('At least one of -f and -e must be specified, '
                         'otherwise there is nothing to do!')
        return 1

    fs = transferer.Transferer(
        confirm_all=args.interactive,
        confirm_overwrite=not args.overwrite,
        keep_originals=args.keep)
    logger.debug('Created transferer: %s', fs)

    try:
        for base in args.base:
            base = base.rstrip('/')  # otherwise will get empty basename
            basename = os.path.basename(base)
            name = util.string_prompt(
                'Name of feature in {0}'.format(basename),
                feature.Feature.translate_name(basename))
            if args.feature:
                feature.Feature(fs).process(base, name, args.feature)
            if args.extras:
                extras.Extras(fs).process(base, name, args.extras)
            if not args.keep and args.feature and args.extras:
                fs.maybe_rmdir(base)
    except IOError as e:
        util.print_error(str(e))
        return 2
    except EOFError:
        return 3

    return 0


def main_cli():
    """
    grymp's command-line entry point.

    :return: The return code of the program.
    """
    status = main(sys.argv)
    logger.debug('Returning exit status %d', status)
    return status


if __name__ == '__main__':
    sys.exit(main_cli())
