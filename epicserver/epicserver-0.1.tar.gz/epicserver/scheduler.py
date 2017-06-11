#!/usr/bin/env python3

from .log import system_log as _log
from . import __version__
from .cmds import Cmd, CmdRPC, CmdSleep, CmdPersist
from .encoders.pickle import Pickle
from .objects import ID
from .log import CmdLog

from itertools import count
from time import monotonic as now
from select import select

import logging
import sys

import gc

log = _log.getChild('scheduler')
stats_log = _log.getChild('stats')

encoder = Pickle('pickle://')

def gen_msg_id():
    i = 0
    while True:
        i += 1
        yield i

class Setup(): pass

def scheduler(entry_point, pool, db, logger):
    setup = entry_point(pool)

    msg_id = gen_msg_id()
    
    run_queue = [((Setup, 'Startup Code'), setup, None, False, None)]
    blocked = {}
    
    out_replies = []
    in_replies = []
    
    out_requests = []
    in_requests = []
    
    sleeping = []
    
    try:
        gc.disable()

        for loop_iter in count():
            wokeup_at = now()
            log.info("Commencing loop %d @ %f", loop_iter, wokeup_at)
            stats = []
            stats.append(('Woken Up', wokeup_at))
            wokeup = [x for x in sleeping if x[0] <= wokeup_at]
            sleeping = [x for x in sleeping if x[0] > wokeup_at]
    
            for wakeup_at, entity_id, context, reply_id in wokeup:
                run_queue.append((entity_id, context, None, False, reply_id))
        
            stats.append(('Incomming Replies', now()))
            # deal with replies
            for val in in_replies:
                reply_id, value, err = encoder.load(val)
                entity_id, context, reply_id = blocked.pop(reply_id)
                run_queue.append((entity_id, context, value, err, reply_id))
    
            stats.append(('Incomming Requests', now()))
            # deal with new incomming requests
            for val in in_requests:
                reply_id, entity_id, method_name, args, kwargs = encoder.load(val)
                entity = pool[entity_id]
                method = getattr(entity, method_name)
                context = method(*args, **kwargs)
                run_queue.append((entity_id, context, None, False, reply_id))
    
            in_replies = []
            in_requests = []
        
            stats.append(('Running Contexts', now()))
            for entity_id, context, value, err, reply_id in run_queue:
                cmd = None
                try:
                    if err:
                        cmd = context.throw(value)
                    else:
                        cmd = context.send(value)
                except StopIteration as ret:
                    if reply_id is not None:
                        out_replies.append((reply_id, ret.value, False))
                except Exception as exc:
                    if reply_id is not None:
                        out_replies.append((reply_id, exc, True))
                    else:
                        log.error("Setup code generated an abnormal exception")
                        raise
                                
                entity_short_name = "{}[{}].{}".format(entity_id[0].__name__, entity_id[1], context.__name__)
                if isinstance(cmd, CmdRPC):
                    log.debug("Grain %s is making an RPC request to %s[%s].%s(%s, %s)", entity_short_name, 
                                                                                        cmd.typ.__qualname__, 
                                                                                        cmd.id, 
                                                                                        cmd.method,
                                                                                        cmd.args, 
                                                                                        cmd.kwargs)
                    request_id = next(msg_id)
                    blocked[request_id] = entity_id, context, reply_id
                    out_requests.append((request_id, (cmd.typ, cmd.id), cmd.method, cmd.args, cmd.kwargs))
    
                elif isinstance(cmd, CmdSleep):
                    log.info('Grain %s is sleeping', entity_short_name)
                    sleeping.append((cmd.wakeup_at, entity_id, context, reply_id))
    
                elif isinstance(cmd, CmdPersist):
                    log.info("Grain %s requested that it be persisted: %s", entity_short_name, cmd.state)
    
                    db[entity_id] = cmd.state
         
                    # reschedle process
                    request_id = next(msg_id)
                    blocked[request_id] = entity_id, context, reply_id
                    out_replies.append((request_id, None, False))
                    
                elif isinstance(cmd, CmdLog):
                    logger(*cmd[:4], *cmd.args, **cmd.kwargs)
                    
                    # reschedle process
                    request_id = next(msg_id)
                    blocked[request_id] = entity_id, context, reply_id
                    out_replies.append((request_id, None, False))

                elif isinstance(cmd, Cmd):
                    log.exception('Grain %s attempted to execute an unknown cmd: %s', entity_short_name, cmd)
            
                    # reschedle process
                    request_id = next(msg_id)
                    blocked[request_id] = entity_id, context, reply_id
                    out_replies.append((request_id, None, False))

            run_queue = []
    
            stats.append(('Outgoing Replies', now()))
            # send out replies
            for reply_id, value, err in out_replies:
                val = encoder.dump((reply_id, value, err))
                in_replies.append(val)
            
            stats.append(('Outgoing Requests', now()))
            # send out new requests rpc
            for reply_id, entity_id, method_name, args, kwargs in out_requests:
                val = encoder.dump((reply_id, entity_id, method_name, args, kwargs))
                in_requests.append(val)
    
            out_replies = []
            out_requests = []
    
            stats.append((None, now()))
            time_spent = []
            for i, stat in enumerate(stats[:-1]):
                name, t1 = stat
                t2 = stats[i+1][1]
                time_spent.append((name, t2-t1))
    
            i = 0
            for name, spent in time_spent:
                stats_log.debug(f"stat:{i} {name}: {spent:.6f}")
                i += 1

            gc.collect(generation=0)
    
            if len(in_replies) == 0 and len(in_requests) == 0:
                gc.collect(generation=2) # try and get a free hit in here for the gc
                
                if sleeping:
                    pause = sleeping[0][0] - now()
                    if pause <= 0:
                        continue
                    log.info("Only sleeping tasks, sleeping for %s for %fs", sleeping[0][1], pause)
                    select([], [], [], pause)
                else:
                    log.info("no tasks... pausing")
                    # give us a 'out' to restart the loop
                    # to see what happens
                    select([sys.stdin.fileno()], [], [])
                    sys.stdin.readline()
    finally:
        gc.enable()
