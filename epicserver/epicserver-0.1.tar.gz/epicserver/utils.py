#!/usr/bin/env python3

from .log import system_log as _log
import importlib

log = _log.getChild('utils')

def load_module(s: str) -> object:
    """Load an object given a file path or module path
    
    Arguments:
        s (str): a string in the format "<module or file>:<function>"
    
    Returns:
        any valid python object
    """
    module_name, func_name  = s.rsplit(":", maxsplit=1)
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        raise
    except Exception as err:
        raise ImportError("Error occured during import") from err
    func = getattr(module, func_name)

    return func
    
    
