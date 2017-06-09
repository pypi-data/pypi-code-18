""" ModPy package. """

__all__ = [ ]

# resource decorators
from .resources import func
from .resources import initial
from .resources import final
from .resources import event
from .resources import proc
from .resources import timer

# API for nodes
from .nodes import init_node
from .nodes import stop_node
from .nodes import self_node
from .nodes import self_nodename
from .nodes import self_nodeaddr
from .nodes import lookup_remote_node
from .nodes import create_remote_node
from .nodes import add_remote_node
from .nodes import remove_remote_node
from .nodes import NODESTAT_INIT
from .nodes import NODESTAT_CONN
from .nodes import NODESTAT_ADDR

# API for resource access
from .funcall import call
from .funcall import callnr
from .funcall import broadcast
from .funcall import waitfor
from .funcall import fire

# Load system modules
from modpy.sysmod import discover
