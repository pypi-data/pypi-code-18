""" Hypershot Configuration.

    Config is only availalble *after* command line parsing,
    so do not access it in top-level code,
    and do not use ``from …`` imports.
"""

def _items():
    """Return a dict of all settings."""
    return {k: v for k, v in globals().items() if not k.startswith('_')}


# Enable debugging features?
debug = False

# Verbose logging?
verbose = False

# Simulate things?
dry_run = False

# Image upload only?
upload = False

# Name of image hosting service
service = ""

# Width of optional thumbnail?
thumb_size = 0

# Configuration only settings (these have no command line equivalent)
services = {}
