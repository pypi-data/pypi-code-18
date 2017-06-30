"""

Arglog
======

Automatically configure an argparse.ArgumentParser with a --loglevel option.

"""

__version__ = '2017.6.1'

from argparse import ArgumentParser
import logging


def patch(parser, default='INFO', basicConfig_kwargs={}):
    # type: (ArgumentParser, str) -> None
    parser.add_argument(
        '-l', '--loglevel', help='Logging level', default=default,
        choices=list(logging._nameToLevel.keys()),
    )

    def configure_logging(args):
        logging.basicConfig(
            level=logging._nameToLevel[args.loglevel],
            **basicConfig_kwargs,
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
