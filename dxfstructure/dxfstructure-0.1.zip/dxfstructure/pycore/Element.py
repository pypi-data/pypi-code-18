'''
--------------------------------------------------------------------------
Copyright (C) 2017 Lukasz Laba <lukaszlab@o2.pl>

File version 0.2 date 2017-06-01
This file is part of DxfStructure (structural engineering dxf drawing system).
http://struthon.org/

DxfStructure is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

DxfStructure is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import os
import random

import ezdxf
from tabulate import tabulate

from geo import Point, Line, Polyline, Rectangle
import x_dxf_test_path

import text_syntax_element

class Element():
    def __init__(self, dxf_pline_entity=None):
        self.dxf_pline_entity = dxf_pline_entity
        self.dxf_text_entity = None
        #---
        self.rectangle = None
        self.barlist = []
        #---
        if self.dxf_pline_entity == None:
            pass
            self.get_test_dxf_pline_entity()
        #---
        self._create_rectangle()

    #----------------------------------------------

    def add_bar(self, bar):
        self.barlist.append(bar)
    
    def clear_data(self):
        self.dxf_text_entity = None
        self.rectangle = None
        self.quantity = 0
        self.barlist = []
    #----------------------------------------------
    
    @property
    def maintext_string(self):
        if self.dxf_text_entity:
            return self.dxf_text_entity.dxf.text
        else:
            return ''
    
    @property
    def name(self):
        if text_syntax_element.has_correct_format(self.maintext_string):
            return text_syntax_element.data_get(self.maintext_string)['Name']
        else:
            return '(not named)'

    @property
    def quantity(self):
        if text_syntax_element.has_correct_format(self.maintext_string):
            return int(text_syntax_element.data_get(self.maintext_string)['Number'])
        else:
            return 1
            
    #----------------------------------------------
    
    def get_bar_number(self):
        return len(self.barlist)    

    #----------------------------------------------

    def _create_rectangle(self):
        plinepoints = list(self.dxf_pline_entity.get_rstrip_points())
        pointsnumber = len(plinepoints)
        xcoords = [i[0] for i in plinepoints]
        ycoords = [i[1] for i in plinepoints]
        corner1 = Point([min(xcoords), max(ycoords)])
        corner2 = Point([max(xcoords), min(ycoords)])
        self.rectangle = Rectangle(corner1, corner2)

    #----------------------------------------------
        
    def __str__(self):
        return 'element - ' + str(self.name) + 'x' +str(self.quantity) + ' with %s'%self.get_bar_number()
    
    #----------------------------------------------
    
    @property
    def schedule_record(self):
        bar_records = []
        for bar in self.barlist:
            bar_records += bar.schedule_record
        bar_records.sort(key=lambda record: int(record[1]), reverse = False) 
        #---
        for i in range(len(bar_records)-1):
            if bar_records[i][1] == bar_records[i+1][1]:
                bar_records[i+1][7] += bar_records[i][7]
                bar_records[i+1][8] += bar_records[i][8]
                bar_records[i+1][9] += bar_records[i][9]
                bar_records[i+1][10] += bar_records[i][10]
                bar_records[i] = None
        while None in bar_records:
            bar_records.remove(None)        
        return bar_records
    
    @property
    def Mass(self):
        mass = sum(bar.Total_Mass for bar in self.barlist)
        mass = round(mass, 2)
        return mass
    
    @property
    def Total_Mass(self):
        mass = self.Mass * self.quantity
        mass = round(mass, 2)
        return mass

    #----------------------------------------------
        
    def get_test_dxf_pline_entity(self):
        #---geting random dxf_pline_entity from example dxf from 
        dwg = ezdxf.readfile(x_dxf_test_path.test_path)
        pline_entity_list = []
        for e in dwg.modelspace():
            if e.dxftype() == 'LWPOLYLINE' and e.dxf.layer == 'DS_ELEMENT':
                pline_entity_list.append(e)
        to_get = random.randint(0, len(pline_entity_list)-1)
        dxf_pline_entity = pline_entity_list[to_get]
        #--- writing to atribute
        self.dxf_pline_entity = dxf_pline_entity

# Test if main            
if __name__ == "__main__":
    from environment import*
    DRAWING.open_file()
    SCANER.load_data_to_model()
    element = CONCRETE_MODEL.elementlist[0]
    for element in CONCRETE_MODEL.elementlist:
        print element.name, element.quantity