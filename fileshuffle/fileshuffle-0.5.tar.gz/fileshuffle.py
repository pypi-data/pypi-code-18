#!/usr/bin/env python3

import argparse
import functools
import os
import random
import re
import shutil

import tqdm

parser = argparse.ArgumentParser(description='Shuffle files')


def dir_exists(dirname):
    if not os.path.exists(dirname):
        raise argparse.ArgumentTypeError('%s does not exist' % dirname)
    if not os.path.isdir(dirname):
        raise argparse.ArgumentTypeError('%s is not a directory' % dirname)
    return dirname


def dir_autocreate(dirname):
    if dirname is None:
        return

    if os.path.exists(dirname):
        if not os.path.isdir(dirname):
            raise argparse.ArgumentTypeError('%s is not a directory' % dirname)
        try:
            shutil.rmtree(dirname)
        except Exception as e:
            print('Error removing %s: %s' % (dirname, e))
            exit(-2)

    os.makedirs(dirname)
    return dirname


parser.add_argument('source', type=dir_exists, help='Source directory')
parser.add_argument('--destination', type=dir_autocreate, required=True,
                    help='Destination directory. Will be cleared if exists and created if not')
parser.add_argument('--recurse', '-R', action='store_true', default=False,
                    help='Search files in source directory recursively')
parser.add_argument('--no-shuffle', action='store_true', default=False, help='Do not shuffle gathered files')
parser.add_argument('--order_prefix', default='{number:0>%(num)s}. {filename}')
parser.add_argument('--order_prefix_regexp', default='^\d+\. ',
                    help='Used to detect existing order prefixes and remove them')

args = vars(parser.parse_args())

source_list = list()

if args['recurse']:
    for dirname, _, filenames in os.walk(args['source']):
        if not len(filenames):
            continue
        print('Found %s files in %s' % (len(filenames), dirname))
        source_list.extend(map(functools.partial(os.path.join, dirname), filenames))

else:
    old_len = len(source_list)
    source_list.extend(
        filter(os.path.isfile, map(functools.partial(os.path.join, args['source']), os.listdir(args['source']))))
    print('Found %s files in %s' % (len(source_list) - old_len, args['source']))

print('Found %s files total' % len(source_list))

if not args['no_shuffle']:
    random.shuffle(source_list)

for n, source_file in tqdm.tqdm(enumerate(source_list), desc='Files processed', total=len(source_list)):
    order_prefix = args['order_prefix'] % {'num': len(str(len(source_list)))}
    filename = os.path.split(source_file)[-1]
    filename = re.sub(args['order_prefix_regexp'], '', filename)
    filename = order_prefix.format(number=n, filename=filename)
    shutil.copy(source_file, os.path.join(args['destination'], filename))
