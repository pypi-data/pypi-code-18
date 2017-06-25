from .yargs import OptionMapper


def parse(name):
    """Ignore arguments from the CLI"""

    parser = OptionMapper(name)
    return parser.parse([])


def parse_main(name, args=None):
    """Merge arguments from the CLI"""

    parser = OptionMapper(name)
    return parser.parse(args)
