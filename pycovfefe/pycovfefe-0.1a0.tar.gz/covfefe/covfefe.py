import os
import sys


def convert(value):
    return u'{0} covfefe'.format(value)


def main():
    if len(sys.argv) > 1:
        print(convert(' '.join(sys.argv[1:])))
    else:
        print('Usage: covfefe <message you want to use>')
