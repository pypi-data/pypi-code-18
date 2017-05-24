import os, logging
from functools import wraps

# =============================================================================
# Constants
# =============================================================================

#: Log formatting constant that uses vt100 escape sequences to produce 
#: highlighted function names and displays the message
LOG_FORMAT_ESCAPED = '\033[1m%(funcName)s\033[0m: %(message)s'

#: Typical log formatting contsant shows date/time, function info, pid/tid and 
#: message
LOG_FORMAT_STANDARD = ('%(asctime)s %(name)s.%(funcName)s: '
    'pid:tid=%(process)d:%(thread)d %(message)s')

# =============================================================================
# Logging Configuration
# =============================================================================

def configure_file_logger(name, log_dir, log_level=logging.DEBUG):
    """Shortcut method that sets up logging to use the 
    :class:`SizeRotatingFileHandler` with the LOG_FORMAT_STANDARD display."""
    from .srothandler import SizeRotatingFileHandler

    root = logging.getLogger()
    root.setLevel(log_level)
    handler = SizeRotatingFileHandler(os.path.join(log_dir, '%s.log' % name))
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT_STANDARD))

    root.addHandler(handler)


def configure_stdout_logger(log_level=logging.DEBUG):
    """Shortcut method that sets up logging to use STDOUT and with the
    LOG_FORMAT_ESCAPED configuration."""
    root = logging.getLogger()
    root.setLevel(log_level)

    handler = logging.StreamHandler()
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(LOG_FORMAT_ESCAPED))

    root.addHandler(handler)


def default_logging_dict(log_dir, handlers=['file'], filename='debug.log'):
    """Returns a logging configuration dictionary with reasonable defaults.
    Defines two handlers: "default" goes to STDOUT using the
    LOG_FORMAT_ESCAPED configuration and "file" uses a
    :class:`SizeRotatingFileHandler` with the LOG_FORMAT_STANDARDD 
    configuration.  Only the "file" hanlder is on by default.

    :param log_dir:
        Directory for logs to go into.
    :param handlers:
        Which logging handlers to use.  Defaults to only 'file'
    :param filename:
        Base name of the file to log to.  Defaults to "debug.log".
    """
    d = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'escaped': {
                'format':LOG_FORMAT_ESCAPED,
            },
            'standard': {
                'format':LOG_FORMAT_STANDARD,
            },
        },
        'handlers': {
            'default': {
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter':'escaped',
            },
            'file': {
                'level':'DEBUG',
                'class':'logthing.srothandler.SizeRotatingFileHandler',
                'filename': os.path.abspath(os.path.join(log_dir, filename)),
                'formatter':'standard',
                'maxBytes':300000,
            },
        },
        'loggers': {
            '': {
                'handlers':handlers,
                'propagate': False,
                'level':'DEBUG',
            },
        },
    }

    return d

# ============================================================================
# Decorators
# ============================================================================

def silence_logging(method):
    """Context wrapper that on entry disables logging and turns it back on
    upon exit.  
    
    Often useful when testing if a test method is supposed to issue an
    error message which is confusing that the error shows for a successful
    test.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        logging.disable(logging.ERROR)
        result = method(*args, **kwargs)
        logging.disable(logging.NOTSET)
        return result
    return wrapper
