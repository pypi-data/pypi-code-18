""" Hypershot Configuration.
"""

def _items():
    """Return a dict of all settings."""
    return {k: v for k, v in globals().items() if not k.startswith('_')}


# Enable debugging features?
debug = False

# Verbose logging?
verbose = False
