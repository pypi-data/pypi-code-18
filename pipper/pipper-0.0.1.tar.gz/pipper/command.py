from pipper import parser
from pipper import installer


def run(cli_args: list = None):
    """ """

    args = parser.parse(cli_args)

    if args['action'] == 'install':
        installer.install_many(args['packages'])
