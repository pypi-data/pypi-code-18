# coding:utf-8
import os
import sys
import hashlib
import traceback
from io import open, BytesIO
import argparse

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'


def main_argv(argv=None, debug=False):
    if argv == None: argv = sys.argv[1:]

    parser = argparse.ArgumentParser(prog='checksum', description='Generate the checksum of a file.')
    parser.add_argument('file', metavar='file', type=str, help='file path')
    parser.add_argument('--hash', metavar='hash', type=str, help='hash method', default='md5')

    args = parser.parse_args(argv)
    if debug:
        print(argv)
        print("file:{args.file}, hash:{args.hash}".format(args=args))
    main(args.file, args.hash)
    pass


def main(filepath, hash):
    err = sys.stderr

    hashsum = ''

    if not os.path.isfile(filepath):
        err.write("Error: Unexist file:{filepath}".format(**locals()))
        err.flush()
        return 1

    f = open(filepath, 'rb')
    try:
        hashsum = generate_hashsum(hash, f)
    except NotImplementedError:
        err.write("Error: Unsuport hash:{hash}".format(**locals()))
        err.flush()
        return 1
    except Exception as e:
        err.write(traceback.format_exc())
        err.flush()
        return 2

    print(hashsum)
    return 0


def generate_hashsum(hash, bytes_stream, buffer_size=1024 * 100):
    if not hash or not hasattr(hashlib, hash):
        raise NotImplementedError

    h = hashlib.new(hash)
    while True:
        data = bytes_stream.read(buffer_size)
        if not data: break
        h.update(data)

    return h.hexdigest()
