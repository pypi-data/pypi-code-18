# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 14:33:13 2017

@author: Yuki
"""

class Base():
    def __init__(self,value):
        print('Base')

class Mul(Base):
    def __init__(self,value):
        super().__init__(value)
        self.value=value
        print('Mul.__init__')
        
    def multiple(self,times):
        self.value=self.value*times
        print(self.value)
        
class Add(Base):
    def __init__(self,value):
        super().__init__(value)
        self.value=value
        print('Add.__init__')
        
    def add(self,times):
        self.value+=times
        print(self.value)
        
class Child(Mul,Add):
    def __init__(self,value):
        super(Child,self).__init__(value)
        print('child')
#        super(Mul,self).__init__(value)
#        Mul.__init__(self,value)
#        Add.__init__(self,value)
        
if __name__=='__main__':
    import inspect
    child=Child(1)
    child.add(1)
    child.multiple(2)