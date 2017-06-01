"""Awaitable IO utility functions for runaway."""


# [ Imports ]
from .ainput import ainput
from .looping import run_forever, do_while


# [ Static Checks ]
assert all((ainput, run_forever, do_while))
