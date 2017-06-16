""" ModPy package. """

__all__ = [ ]

# resource decorators
from .resources import func
from .resources import initial
from .resources import final
from .resources import event
from .resources import proc

# resource creation
from .resources import Event
from .resources import create_event

# API for nodes
from .nodes import init_node
from .nodes import stop_node
from .nodes import self_node
from .nodes import self_nodename
from .nodes import self_nodeaddr

# API for resource access
from .funcall import call
from .funcall import callnr
from .funcall import broadcast
from .funcall import waitfor
from .funcall import fire

# Load system modules
from modpy.sys import discover
