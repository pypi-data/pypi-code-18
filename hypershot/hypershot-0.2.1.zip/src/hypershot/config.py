# pylint: disable=invalid-name
""" Hypershot Configuration.

    Config is only availalble *after* command line parsing,
    so do not access it in top-level code,
    and do not use ``from …`` imports.
"""
import logging

def items():
    """Return a dict of all settings."""
    return {k: v
            for k, v in globals().items()
            if (not k.startswith('_')
                and k not in {'log'}
                and not callable(v)
                and not hasattr(v, '__package__')
               )
           }


#############################################################################
# Settings with a command line equivalent

# Enable debugging features?
debug = False

# Hide result output?
quiet = False

# Verbose logging?
verbose = False

# Simulate things?
dry_run = False

# No progress display?
no_progress, progress = False, True

# Name of image hosting service
service = "imgur"

# Name of chosen template
template = "bbcode"

# Path to configuration (valid after CLI options parsing)
config_dir = None

# Width of optional thumbnail?
thumb_size = 0


#############################################################################
# Configuration only settings (these have no command line equivalent)

# Terminal table style (one of: bare, ascii, single, double)
table_style = 'single'
table_class = None  # initialized based on 'table_style'

# Write JSON files?
json_files = True

# Global application logger (replaced early in CLI setup, after options parsing)
log = logging.getLogger()

# Services as defined in 'config.yaml'
services = {}
