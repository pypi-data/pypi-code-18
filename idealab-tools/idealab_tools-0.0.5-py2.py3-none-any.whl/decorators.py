# -*- coding: utf-8 -*-
"""
Created on Thu May 25 08:44:45 2017

@author: daukes
"""

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate
