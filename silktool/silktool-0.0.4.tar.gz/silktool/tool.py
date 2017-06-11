"""This file will have all the instructions to create the new tool setup."""

from util import Tooler


def print_hello():
    """Method is signature Hello world method for this project."""
    return 'Binu Says Hello!!!!'


def start_tool(parser, context, args):
    """Method to start a new package tool."""
    t = Tooler()
    if isinstance(args, list) or isinstance(args, tuple) and len(args)>0:
        t.mkpkg(args[0])
    elif isinstance(args, str):
        t.mkpkg(args)
    else:
        raise Exception('Unable to create package!')
