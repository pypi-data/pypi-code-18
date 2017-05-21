# -*- coding: utf-8 -*-
"""
Created on Mon May 15 21:26:18 2017

@author: Press150
"""

import visa

class GpibInst():
    def __init__(self,gpib=9):
        self.gpib = int(gpib)
        rm=visa.ResourceManager()
        self.inst = rm.get_instrument("GPIB::"+ str(self.gpib))    
        
    def query(self,command,raw_string=False):
        answer=self.inst.ask('DATA?')
        if raw_string:
            return answer
        else:
            answer=answer.strip('\n')
            answer=answer.strip('\r')
            return float(answer)
    
    def write(self,command):
        return self.inst.ask('DATA?')