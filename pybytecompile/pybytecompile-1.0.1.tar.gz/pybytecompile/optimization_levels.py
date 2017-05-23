"""Underlying library for pybytecompile script
"""

from enum import Enum


class OptimizationLevel(Enum):
    """The levels as understood by compileall
    """
    NONE = 0
    PARTIAL = 1
    FULL = 2
