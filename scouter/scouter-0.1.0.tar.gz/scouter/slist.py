#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Scouter List
  Created: 05/24/17
"""

import traceback

from . import sbase

########################################################################
class SList(sbase.SBase):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, value, 
                 add_new_item_callback=None,
                 del_new_item_callback=None,
                 new_list_value_callback=None):
        """"""
        assert isinstance(value, list)
        
        self._value = value
        
        self._anic = add_new_item_callback
        self._dnic = del_new_item_callback
        self._nlv = new_list_value_callback
    
    @property
    def value(self):
        """"""
        return self._value
    
    @value.setter
    def value(self, new):
        """"""
        assert isinstance(new, list)
        
        orig = self._value
        self._value = new
        if self._nlv:
            self._nlv(new, orig)
        
    
    #----------------------------------------------------------------------
    def append(self, obj):
        """"""        
        self._value.append(obj)
        if self._anic:
            self._anic(obj, -1)        
        
        
        
    #----------------------------------------------------------------------
    def extend(self, iterable):
        """"""
        for i in iterable:
            self.append(i)
    
    #----------------------------------------------------------------------
    def insert(self, index, obj):
        """"""
        if self._anic:
            self._anic(obj, index)
        
        self._value.insert(index, obj)
        
        
    #----------------------------------------------------------------------
    def pop(self, index):
        """"""
        obj = self._value.pop(index)
        if self._dnic:
            self._dnic(obj, index)        
        
    #----------------------------------------------------------------------
    def remove(self, value):
        """"""
        self._value.remove(value)
        if self._dnic:
            self._dnic(value, self._value.index(value))
        
    
    #----------------------------------------------------------------------
    def count(self, value):
        """"""
        return self._value.count(value)
    
    #----------------------------------------------------------------------
    def index(self, value, start=None, stop=None):
        """"""
        return self._value.index(value)
    
    #----------------------------------------------------------------------
    def reverse(self):
        """"""
        return self._value.reverse()
    
    #----------------------------------------------------------------------
    def sort(self, cmp=None, key=None, reverse=False):
        """"""
        return self._value.sort(cmp, key, reverse)

    #----------------------------------------------------------------------
    def __setitem__(self, key, value):
        """"""
        self._value[key] = value
        if self._anic:
            self._anic(value, key)        
        
    
    #----------------------------------------------------------------------
    def __getitem__(self, key):
        """"""
        return self._value[key]
    
    #----------------------------------------------------------------------
    def __delitem__(self, key):
        """"""
        obj = self._value[key]
        del self._value[key]
        
        if self._dnic:
            self._dnic(obj, key)
        
    
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        self._listiter = iter(self._value)
        return self._listiter
    
    #----------------------------------------------------------------------
    def next(self):
        """"""
        return self._listiter.next()
        
        
        