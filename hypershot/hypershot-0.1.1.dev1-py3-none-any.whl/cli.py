"""
    Create screen shots of a video file, and upload them to an image host.

    Usage:
        hypershot [options] <video>
        hypershot (-h | --help)
        hypershot --version

    Options:
        -h, --help                  Show this screen.
        --version                   Show version.
        --debug                     Enable debugging features?
        -v, --verbose               Verbose logging?
        -c PATH, --config-dir=PATH  Custom configuration directory.
"""
import os
import sys
import textwrap

import appdirs
from addict import Dict as attrdict
from docopt import docopt

from . import config
from . import __name__ as appname, __version__, section


def parse_args():
    """Return command line options and arguments."""
    location = os.path.commonprefix([__file__, os.path.realpath(sys.argv[0]), sys.prefix])
    location = (location + os.sep).replace(os.path.expanduser('~' + os.sep), '~' + os.sep)
    location = location.rstrip(os.sep)
    version_info = '{} {}{}{} using Python {}'.format(
                   appname, __version__,
                   ' from ' if location else '', location,
                   sys.version.split()[0])

    mixed = docopt(textwrap.dedent(__doc__), version=version_info)
    options, args = {}, {}
    for key, val in mixed.items():
        name = key.replace('-', '_')
        if key.startswith('--'):
            options[name[2:]] = val
        elif key.startswith('-'):
            options[name[1:]] = val
        elif key.startswith('<') and key.endswith('>'):
            args[name[1:-1]] = val
        else:
            raise ValueError('Internal error: Invalid docopt key "{}"'.format(key))

    return attrdict(options), attrdict(args)


def coerce_to_default_type(key, val, default_val):
    """Coerce a given string to the type of a default value."""
    if not isinstance(val, str):
        return val

    newval = val
    try:
        if isinstance(default_val, bool):
            newval = val.lower() in ('1', 'true', 'on', 'enable', 'enabled')
            if newval is False and val.lower() not in ('0', 'false', 'off', 'disable', 'disabled'):
                raise ValueError("Expecting a true/false value")
        elif isinstance(default_val, int):
            newval = int(val)
        # TODO: elif isinstance(default_val, list):
        # TODO: elif isinstance(default_val, dict):
    except (TypeError, ValueError) as cause:
        raise ValueError('Bad value "{val}" for key "{key}": {cause}'.format(
                         key=key, val=val, cause=cause)) from None

    return newval


def parse_config(options):
    """Populate 'config' module from configuration file, the environment, and CLI options."""
    # Read a config file, if found
    config_dir = appdirs.user_config_dir(appname, section)
    config_dir = os.environ.get('HYPERSHOT_CONFIG_DIR', config_dir)
    config_dir = options.config_dir or config_dir
    if options.debug:
        print("TRACE Configdir:", config_dir)
    config_vals = {}
    # TODO: Actually read file

    # Override config defaults from command line, environment, or config file
    for key, default_val in vars(config).items():
        if key.startswith('_'):
            continue

        val, scope = None, ''
        env_key = ('{}_{}'.format(appname, key)).upper()
        if options.get(key) not in (None, False):
            val, scope = options[key], 'cli::'
        elif env_key in os.environ:
            val, scope = os.environ[env_key], 'env::'
        elif key in config_vals:
            val, scope = config_vals[key], 'cfg::'

        if val is not None:
            setattr(config, key, coerce_to_default_type(scope + key, val, default_val))


def run():
    """The CLI entry point."""
    options, args = parse_args()
    if options.debug:
        print("TRACE Options + args:", options, args)

    parse_config(options)
    if config.debug:
        print("TRACE Configuration:", config._items())
