#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: SVar
  Created: 05/24/17
"""

from . import sbase

########################################################################
class SVar(sbase.SBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, value, callback=None):
        """Constructor"""
        self._callback = callback
        if self._callback:
            assert callable(callback), 'the callback is not callable'
        
        self._value = value
        
    @property
    def value(self):
        """"""
        return self._value

    @value.setter
    def value(self, new_value):
        """"""
        _r = None
        
        #
        # if callback exsited execute callback
        #
        if self._callback:
            _r = self._callback(new_value, self.value)
        
        if _r:
            self._value = _r
        else:
            self._value = new_value

    
            
        
        
    
    