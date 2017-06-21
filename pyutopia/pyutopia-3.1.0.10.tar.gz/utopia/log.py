import logging
logger = logging.getLogger(__package__)
logger.addHandler(logging.NullHandler())
__all__ = ['logger']