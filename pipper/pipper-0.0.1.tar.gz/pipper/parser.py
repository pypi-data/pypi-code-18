import os
import sys
from argparse import ArgumentParser

package_directory = os.path.dirname(os.path.realpath(__file__))


def read_file(*args) -> str:
    """ """

    path = os.path.join(package_directory, *args)
    with open(path, 'r') as f:
        return f.read()


def populate_install(parser: ArgumentParser) -> ArgumentParser:
    """ """

    parser.description = read_file('resources', 'install_command.txt')

    parser.add_argument(
        'packages',
        nargs='+'
    )

    return parser


def parse(cli_args: list = None) -> dict:
    """ """

    parser = ArgumentParser(
        description=read_file('resources', 'command_description.txt'),
        add_help=True
    )

    subparsers = parser.add_subparsers(help='Command actions', dest='action')

    populate_install(subparsers.add_parser('install'))

    return vars(parser.parse_args(cli_args))
