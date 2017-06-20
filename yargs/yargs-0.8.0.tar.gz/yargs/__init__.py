from .yargs import OptionMapper


def parse(name):
    parser = OptionMapper(name)
    return parser.parse()
