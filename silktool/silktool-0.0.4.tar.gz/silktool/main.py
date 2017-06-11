import sys

from argparse import RawDescriptionHelpFormatter
from arghandler import ArgumentHandler
from textwrap import dedent
from tool import start_tool


DESCRIPTION = dedent("""
    Tooler Help
    =================

    Commonly Used Commands:
        * start: This command is used to start a new tool setup. takes tool name as argument.
    """)


def main(args=sys.argv[1:]):
    """Main Method to take inputs from user and route to corresponding functions."""
    handler = ArgumentHandler(
        epilog=DESCRIPTION,
        formatter_class=RawDescriptionHelpFormatter,
    )
    handler.set_subcommands({
        'start': start_tool,
    })
    handler.run(args)


if __name__ == '__main__':
    main()