"""Runaway actions."""


# [ Imports ]
from collections import namedtuple


# [ API ]
Send = namedtuple('Send', 'coro value source')
Throw = namedtuple('Throw', 'coro exc_info source')
Close = namedtuple('Close', 'coro source')
