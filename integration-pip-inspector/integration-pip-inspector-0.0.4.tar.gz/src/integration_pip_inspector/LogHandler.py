from __future__ import print_function
import sys
import traceback

DEBUG = True

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def info(message):
    print(str(message))


def error(message=None, e_message=None, print_exception=DEBUG, exit=False):
    if message:
        print("ERROR >>>>>> " + str(message))
    if e_message and print_exception:
        print(e_message)
    if exit:
        eprint("integration_pip_inspector failed")
        sys.exit(1)


def debug(message=None, exit=False):
    if DEBUG:
        if message:
            print("DEBUG >>>>>> " + str(message))
        if exit:
            eprint("integration_pip_inspector failed")
            sys.exit(1)
