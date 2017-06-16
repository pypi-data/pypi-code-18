import sys
import asyncio

import modpy

cmd_call = None

def normalize(arg):
    try:
        if (len(arg) == 0):
            return arg
        elif arg[0] == '"' and arg[-1] == '"':
            return arg[1:-1]
        else:
            return int(arg)
    except Exception as e:
        raise e

def broadcast(loop, resource, *args):
    try:
        bcast_coro = modpy.broadcast(resource, *args)
        future = asyncio.run_coroutine_threadsafe(bcast_coro, loop)

    except Exception as e:
        raise e

def run_cmd_bcast(cmd, selfnode, *vargs):
    args = vargs[0]
    if (len(args) < 1):
        print(cmd.usage)
        return

    try:
        res = args[0]
        callargs = list(map(normalize, args[1:]))
        broadcast(selfnode.event_loop(), res, *callargs)
    except Exception as e:
        print('Broadcast Error:', e)

    return 1

