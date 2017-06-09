#!/usr/bin/env python

import sys
import argparse

__version__ = '0.1.0'

# parses CLI arguments
def parse_args():
    parser = argparse.ArgumentParser(description='CLI tool for comparing .env files')
    parser.add_argument('files', metavar='FILE', nargs=2, help='env file paths')
    args = parser.parse_args()
    return args.files[0], args.files[1]


# parses a file into an array of lines
def parse_lines(file):
    try:
        return [line for line in open(file)]
    except IOError:
        print('Could not read file:', file)
        sys.exit()


# parses keys (variables) from each file line
def parse_key(line):
    try:
        return line.split('=')[0]
    except IndexError:
        print('Invalid env file. Line missing = operator')
        sys.exit()


# extracts missing lines between files
def get_missing_keys(file_a, file_b):
    missing_keys = list()
    for line_b in parse_lines(file_b):
        if line_b.find('#') == 0:
            continue
        key_b = parse_key(line_b)
        exists = False
        for line_a in parse_lines(file_a):
            key_a = parse_key(line_a)
            if key_b == key_a:
                exists = True
        if not exists:
            missing_keys.append(line_b)

    return missing_keys


def main():
    file_a, file_b = parse_args()
    for line in get_missing_keys(file_a, file_b):
        sys.stdout.write('%sMissing variable%s %s' % ('\033[95m', '\033[0m', line))


if __name__ == '__main__':
    main()
