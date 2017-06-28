#!/usr/bin/env python

# ===============================================================================
# Copyright 2017 GustavoJunior
# ===============================================================================

import argparse
from datetime import datetime

import download


def create_parser():

    parser = argparse.ArgumentParser(prog='cloudsat', description='Download and unzip landsat data.')

    parser.add_argument('--file', help='Name Scene_ID', type=str)
    parser.add_argument('-o', '--output', help='Output directory')
    parser.add_argument('--credentials',
                        help='Path to a text file with USGS credentials with one space between <username password>')
    return parser


def main(args):
    if args:
        print '\nCloudCRM Download SCENE_ID...'
        print args
        download.down_usgs_by_id(args.file,args.output,args.credentials)
    else:
        raise NotImplementedError('Was not executed.')


def __main__():

    global parser
    parser = create_parser()
    args = parser.parse_args()
    exit(main(args))


if __name__ == '__main__':
    try:
        __main__()

    except KeyboardInterrupt:
        exit(1)

# ===============================================================================
