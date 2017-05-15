#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 by Christian Tremblay, P.Eng <christian.tremblay@servisys.com>
# Licensed under LGPLv3, see file LICENSE in this source tree.
#
'''
debug.py - Helper functions to log debug and exception messages

'''

#--- standard Python modules ---
from functools import wraps
import inspect

#--- 3rd party modules ---
#--- this application's modules ---

#------------------------------------------------------------------------------

_DEBUG = 1

def debug(func):
    if 'debug' in inspect.getargspec(func).args:
        raise TypeError('debug argument already defined')
        
    @wraps(func)
    def wrapper(*args, debug=False, **kwargs):
        if debug:
            print('Calling', func.__name__)
        return func(*args, **kwargs)

    
    sig = inspect.signature(func)
    parms = list(sig.parameters.values())
    parms.append(inspect.Parameter('debug',
                                   inspect.Parameter.KEYWORD_ONLY,
                                   default=False))
    wrapper.__signature__ = sig.replace(parameters=parms)                              
    return wrapper                            


def log_debug(cls,txt, *args):
    """
    Helper function to log debug messages
    """
    if _DEBUG:
        msg= (txt % args) if args else txt
        # pylint: disable=E1101,W0212
        cls._debug(msg)


def log_exception(cls,txt, *args):
    """
    Helper function to log debug messages
    """
    msg= (txt % args) if args else txt
    # pylint: disable=E1101,W0212
    cls._exception(msg)
