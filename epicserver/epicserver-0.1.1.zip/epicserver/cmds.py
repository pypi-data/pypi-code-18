#!/usr/bin/env python3

from functools import wraps
from typing import NamedTuple, Iterator, Any, Callable
from types import coroutine
from time import monotonic as now
import logging

class Cmd(NamedTuple):
    pass

class CmdRPC(NamedTuple, Cmd):
    typ: type
    id: 'ID'
    method: None
    args: tuple
    kwargs: dict
    
class CmdSleep(NamedTuple, Cmd):
    wakeup_at: int
        
class CmdPersist(NamedTuple, Cmd):
    state: object

@coroutine
def sleep(delay=0, till=0):
    start = till or now()
    start += delay

    yield CmdSleep(start)

    # we want negative numbers for too early
    jitter = now() - start
    log.debug("Scheduling jitter: %f", jitter)

@coroutine
def persist(state) -> Iterator[CmdPersist]:
    if isinstance(state, Entity):
        state = state.save()
    yield CmdPersist(state)

def auto_persist(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> Any:
        ret = await func(*args, **kwargs)
        await persist(self)
        return ret
    return wrapper

# we have a import loop with objects command
# so dont import until required object are set
# up and ready to be used
from .objects import Entity

from .log import system_log as _log
log = _log.getChild('cmds')
