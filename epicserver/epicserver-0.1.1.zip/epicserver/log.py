#!/usr/bin/env python3.6
"""Logging: loggign abstraction to allow for pluggable backends"""

######
# This is ner the top due to a circular import issue
# by ensuring the __required__ objects are created
# before the import loop we break the cycle
from . import __progname__ as name
import logging

system_log = logging.getLogger(name)
formatter = logging.Formatter("%(asctime)10s %(name)-20s %(levelname)-8s %(message)s")
######

from .cmds import Cmd

from typing import NamedTuple, Callable
from enum import IntEnum, auto
from time import monotonic as now
from functools import wraps
from types import coroutine



class LogLevel(IntEnum):
    debug = auto()
    info = auto()
    warn = auto()
    error = auto()
    exception = auto()


class CmdLog(NamedTuple, Cmd):
    time: float
    name: str
    level: LogLevel
    msg: str
    args: tuple
    kwargs: dict


class Log():
    def __init__(self, name: str) -> None:
        self.name = name
        
    def __getitem__(self, name: str):
        return type(self)(f'{self.name}.{name}')

    @coroutine
    def __call__(self, level: LogLevel, msg: str, *args, **kwargs):
        yield CmdLog(now(), self.name, level, msg, args, kwargs)

    def debug(self, msg: str, *args, **kwargs):
        return self.__call__(LogLevel.debug, msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        return self.__call__(LogLevel.info, msg, *args, **kwargs)

    def warn(self, msg: str, *args, **kwargs):
        return self.__call__(LogLevel.warn, msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        return self.__call__(LogLevel.error, msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        return self.__call__(LogLevel.exception, msg, *args, **kwargs)




def log_filter(level: LogLevel, func) -> Callable[[float, str, LogLevel, str, tuple, dict], None]:
    @wraps(func)
    def filter(time: float, name: str, msg_level: LogLevel, msg: str, *args, **kwargs) -> None:
        if msg_level >= level:
            func(time, name, msg_level, msg, *args, **kwargs)
    return filter


def print_logger(time: float, name: str, msg_level: LogLevel, msg: str, *args, **kwargs) -> None:
    msg = msg.format(*args, **kwargs)
    print(f"{time:.06f} {name:<10} {msg_level.name:<10} {msg}")


def test():
    log = Log('test')
    log_child = log['child']
    
    print = print_log(LogLevel.debug)
    print(*next(log.warn('This is a message')))

    def run(task):
        task = task()
        msg = task.send(None)
        print(*msg)
    
    async def example():
        await log.warn('This is a message')
    
    # should print the msg tuple
    run(example)    

    

if __name__ == "__main__":
    test()
