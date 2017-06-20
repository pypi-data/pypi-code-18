import os
import yaml
import types
import logging
from collections import defaultdict

from argparse import ArgumentParser


OVERWRITE = 'local'


class OptionMapper(object):

    def __init__(self, filename, basedir=None):
        self._filename = filename or 'app_settings'
        self._basedir = basedir or os.getcwd()
        self._build_type = os.getenv('YARGS_ENV', 'dev')

    def _path(self, *parts):
        base = '.'.join(parts)
        full = "%s.yml" % base
        return os.path.join(self._basedir, full)

    def parse(self, args=None):
        paths = [
            self._path(self._filename),
            self._path(self._filename, self._build_type),
            self._path(self._filename, self._build_type, OVERWRITE)
        ]
        options = _merge({}, map(yaml2options, paths))
        parser = generate_parser(options)
        namespace = parser.parse_args(args)
        return namespace


def generate_parser(options):
    """Construct commandline arguments from options dict
    """

    parser = ArgumentParser()
    for name, data in options.iteritems():
        value = data.get("value")
        help = data.get("help")
        choices = data.get("choices")
        list_ = data.get("list")

        if isinstance(value, types.BooleanType):
            # store_true API is a spacial case; it can't be used with the kw varible below
            parser.add_argument("--{}".format(name), help=help,
                                default=value, action='store_true')
        elif list_:
            kw = dict(
                type=type(list_[0]),
                default=list_,
                metavar=value,
                nargs='+',
                help=help
            )
            parser.add_argument("--{}".format(name), **kw)

        elif choices:
            kw = dict(
                type=type(value),
                default=value,
                # metavar=value,
                choices=choices,
                help=help,
            )
            parser.add_argument("--{}".format(name), **kw)
        else:
            kw = dict(
                type=type(value),
                default=value,
                metavar=value,
                choices=choices,
                help=help,
            )
            parser.add_argument("--{}".format(name), **kw)

    return parser


def yaml2options(path):
    options = defaultdict(dict)
    try:
        with open(path) as f:
            src = yaml.load(f, yaml.CLoader)
            for key, value in src.iteritems():
                name, meta = _split(key)
                # Read value from an external file
                if meta == 'txt':
                    options[name]['value'] = _read_text(value)
                else:
                    options[name][meta] = value
    except IOError as e:
        pass
    return options


def _split(key):
    parts = key.split('__')
    if len(parts) == 1:
        parts.append("value")
    return parts


def _merge(target, dicts):
    for d in dicts:
        target.update(d)
    return target


def _read_text(path):
    with open(path) as f:
        return f.read().strip()
