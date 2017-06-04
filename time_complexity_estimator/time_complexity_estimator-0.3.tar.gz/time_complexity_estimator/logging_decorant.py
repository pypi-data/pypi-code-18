import functools
import logging


class LogWith(object):
    """Logging decorator that allows you to log with a
    specific logger.
    """

    ENTRY_MESSAGE = 'Entering {}'
    EXIT_MESSAGE = 'Exiting {}'

    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        """Returns a wrapper that wraps func.
        The wrapper will log the entry and exit points of the function
        with logging.INFO level.
        """
        # set logger if it was not set earlier
        if not self.logger:
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            self.logger.info(
                self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            f_result = func(*args, **kwds)
            self.logger.info(
                self.EXIT_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to
            return f_result

        return wrapper
