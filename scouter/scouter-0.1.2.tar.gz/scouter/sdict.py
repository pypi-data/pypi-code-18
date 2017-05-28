#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: SDict
  Created: 05/24/17
"""

########################################################################
class SDict(dict):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, value, 
                 new_kv_callback=None,
                 del_kv_callback=None,
                 new_value_callback=None):
        """Constructor"""
        #
        # wrap dict object
        #
        assert isinstance(value, dict)
        self._value = value
        
        #
        # set callback
        #
        self._nkvc = new_kv_callback
        self._dkvc = del_kv_callback
        self._nvc = new_value_callback
    
    @property
    def value(self):
        """"""
        return self._value
    
    @value.setter
    def value(self, value):
        """"""
        assert isinstance(value, dict)
        
        orig = self._value 
        self._value = value
        if self._nvc:
            self._nvc(value, orig)
        
    
    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """"""
        self._value[key] = value
        
        if self._nkvc:
            self._nkvc(key, value)
    
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        """"""
        value = self._value[key]
        del self._value[key]
        
        if self._dkvc:
            self._dkvc(key, value)
    
    #----------------------------------------------------------------------
    def __getitem__(self, k):
        """"""
        return self._value[k]
    
    #----------------------------------------------------------------------
    def clear(self):
        """"""
        return self._value.clear()
    
    #----------------------------------------------------------------------
    def copy(self):
        """"""
        _d = self._value.copy()
        
        return SDict(_d, self._nkvc, self._dkvc, self._nvc)
    
    #----------------------------------------------------------------------
    def get(self, k, d=None):
        """"""
        return self._value.get(k, d)

    #----------------------------------------------------------------------
    def has_key(self, k):
        """"""
        return self._value.has_key(k)
    
    #----------------------------------------------------------------------
    def items(self):
        """"""
        return self._value.items()
    
    #----------------------------------------------------------------------
    def iteritems(self):
        """"""
        return self._value.iteritems()

    #----------------------------------------------------------------------
    def iterkeys(self):
        """"""
        return self._value.iterkeys()
    
    #----------------------------------------------------------------------
    def itervalues(self):
        """"""
        return self._value.itervalues()
    
    #----------------------------------------------------------------------
    def keys(self):
        """"""
        return self._value.keys()
    
    #----------------------------------------------------------------------
    def values(self):
        """"""
        return self._value.values()
    
    #----------------------------------------------------------------------
    def pop(self, k, d=None):
        """"""
        return self._value.pop(k, d)
    
    #----------------------------------------------------------------------
    def popitem(self):
        """"""
        return self._value.popitem()
    
    #----------------------------------------------------------------------
    def setdefault(self, k, d):
        """"""
        return self._value.setdefault(k, d)
    
