"""

Arglog
======

Automatically configure an argparse.ArgumentParser with a --loglevel option.

"""

__version__ = '2017.6.2'

from argparse import ArgumentParser
import logging


try:
    # Python 3
    _level_names = logging._nameToLevel
except:
    # Python 2
    _level_names = logging._levelNames


def patch(parser, default='INFO', basicConfig_kwargs=None):
    # type: (ArgumentParser, str) -> None
    basicConfig_kwargs = basicConfig_kwargs or {}
    parser.add_argument(
        '-l', '--loglevel', help='Logging level', default=default,
        choices=list(_level_names.keys()),
    )

    def configure_logging(args):
        logging.basicConfig(
            level=_level_names[args.loglevel],
            **basicConfig_kwargs
        )

    original_parse_args = parser.parse_args
    original_parse_known_args = parser.parse_known_args

    def new_parse_args(*args, **kwargs):
        args = original_parse_args()
        configure_logging(args)
        return args

    def new_parse_known_args(*args, **kwargs):
        args, unknown_args = original_parse_known_args()
        configure_logging(args)
        return args, unknown_args

    parser.parse_args = new_parse_args
    parser.parse_known_args = new_parse_known_args
