import sys
import asyncio

import modpy

cmd_call = None

def normalize(arg):
    if (len(arg) == 0):
        return arg
    elif arg[0] == '"' and arg[-1] == '"':
        return arg[1:-1]
    else:
        return int(arg)

def callback(fut):
    sys.stdout.write('Result: %r\n' % fut.result())
    sys.stdout.write('MODPY> ')
    sys.stdout.flush()

def callback(fut):
    sys.stdout.write('Result: %r\n' % fut.result())
    sys.stdout.write('MODPY> ')
    sys.stdout.flush()

def run_cmd_sub(cmd, loop, *vargs):
    args = vargs[0]
    if (len(args) < 2):
        print(cmd.usage)
        return

    node = args[0]
    res = args[1]

    try:
        modpy.ext_sub_cb(callback, node, res)
    except Exception as e:
        print('Error:', e)

    return 1

