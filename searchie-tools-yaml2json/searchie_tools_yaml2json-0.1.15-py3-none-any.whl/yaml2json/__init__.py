#!/usr/bin/env python3.6
from __future__ import print_function
__all__ = ["yaml2json", "main", "__version__"]

import argparse
import json
import os
import sys
from .version import __version__


def show_version_and_exit():
    print("yaml2json {}".format(__version__))
    sys.exit(0)


def parse_args():
    parser = argparse.ArgumentParser(description="Simple utility to transform yaml files to json format")
    parser.add_argument("--version", dest="show_version", action="store_true")
    parser.add_argument(dest="yaml_in_files", metavar="INPUT-FILE", help=".yml filename which desired to be transformed", default=None, nargs="*")
    parser.add_argument("-q", dest="quiet_mode", action="store_true", help="be quiet")
    parser.add_argument("-o", dest="json_out_file", required=False, default=None, metavar="OUTPUT-FILE", help="json filename to output; use \"-\" for stdout output (\"<infile>.json\" used by default)")
    opts = parser.parse_args()
    if opts.show_version:
        show_version_and_exit()
    if not opts.yaml_in_files or len(opts.yaml_in_files) != 1:
        parser.error("you must specify input file")
    opts.yaml_in_file = opts.yaml_in_files[0]
    return opts


def make_unclosable(buffer):
    class unclosable_wrapper(object):
        def __enter__(self):
            return self
        def __exit__(self, et, ev, etb):
            self.wrapped_object.flush()
        def __init__(self, buffer):
            self.wrapped_object = buffer
        def __getattr__(self, attr):
            return getattr(self.wrapped_object, attr)
        def __setattr__(self, attr, value):
            if attr == "wrapped_object":
                self.__dict__["wrapped_object"]  = value
            elif attr == "__dict__":
                object.__setattr__(self, "__dict__", value)
            else:
                setattr(self.wrapped_object, attr, value)
    return unclosable_wrapper(buffer)


def universal_open(filename, mode="rt"):
    if filename == "-":
        if mode == "rt":
            return make_unclosable(sys.stdin)
        if mode == "wt":
            return make_unclosable(sys.stdout)
        raise AttributeError()
    return open(filename, mode)


def main():
    opts = parse_args()
    if opts.yaml_in_file == "-" and opts.json_out_file is None:
        return yaml2json("-", "-", True)
    return yaml2json(opts.yaml_in_file, opts.json_out_file, opts.quiet_mode)


def yaml2json(yaml_infile, json_outfile=None, quiet_mode=False):
    import yaml
    data = yaml.load(universal_open(yaml_infile))
    out_filename = json_outfile or os.path.extsep.join([os.path.splitext(yaml_infile)[0], 'json'])
    if not quiet_mode:
        print("writing result to {}".format(out_filename), file=sys.stderr)
    with universal_open(out_filename, "wt") as out:
        json.dump(data, indent=2, ensure_ascii=False, fp=out)
        print(file=out)


if __name__ == "__main__":
    main()
