'''
--------------------------------------------------------------------------
Copyright (C) 2015-2017 Lukasz Laba <lukaszlab@o2.pl>

File version 0.1 date 2017-15
This file is part of dxfstructure.
dxfstructure is a range of free open source structural engineering design 
Python applications.
http://struthon.org/

Dxfstructure is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Dxfstructure is distributed in the hope that it will be useful,
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

from geo import Point, Line, Polyline, Bar_shape, pline_from_dxfpline, dim_round
import x_dxf_test_path
import text_syntax_bar
import rcbar_prop
import schedule_format


class Bar():
    def __init__(self, dxf_pline_entity=None):
        self.dxf_pline_entity = dxf_pline_entity
        self.pline = None
        self.element = None
        self.maintext = None
        self.rangepline = None
        self.deptexts = []
        self.delete_mark = False
        #---
        if self.dxf_pline_entity == None:
            self.get_test_dxf_pline_entity()
        #---
        self._create_pline()
    
    #----------------------------------------------
    
    def _create_pline(self):
        self.pline = pline_from_dxfpline(self.dxf_pline_entity)      
        
    #----------------------------------------------
    
    def refresh(self):
        self.data_set()
        self._count_number_for_maintext()
        

    #----------------------------------------------

    def data_set(self, newNumber=None, newType=None, newSize=None, newMark=None):
        #print self.maintext_string
        if newNumber == None: newNumber = None
        if newType == None: newType = self.Type
        if newSize == None: newSize = self.Size
        if newMark == None: newMark = self.Mark
        #---
        text_entity_to_change = self.deptexts + [self.maintext]
        #---
        for dxftxt in text_entity_to_change:
            new_dxftxt_string = text_syntax_bar.data_change(  dxftxt.dxf.text, 
                                                                newNumber=newNumber, 
                                                                newType=newType, 
                                                                newSize=newSize, 
                                                                newMark=newMark )
            dxftxt.dxf.text = new_dxftxt_string     
        #print self.maintext_string
    
    #----------------------------------------------
    
    def _count_number_for_maintext(self):
        #print self.maintext_string
        # from deptexts
        number_list = [text_syntax_bar.data_get(text)['Total_Number'] for text in self.deptexts_list]
        #print number_list
        total_from_deptexts = sum(number_list)
        # from rangepline
        maintext_Centre = self.maintext_data['Centre']
        total_from_rangepline = 0
        if self.rangepline and maintext_Centre:
            #print 'liczymy ilocccccc'
            total_from_rangepline = int(self.rangepline.length / maintext_Centre) + 1
            #print total_from_rangepline, 'total_from_rangepline'
        total = total_from_deptexts + total_from_rangepline
        if total:
            new_maintext = text_syntax_bar.data_change(self.maintext_string, newNumber = total)
            self.maintext.dxf.text = new_maintext
        #print self.maintext_string

    #----------------------------------------------
    
    @property
    def maintext_string(self):
        return self.maintext.dxf.text
        
    @property
    def maintext_data(self):
        return text_syntax_bar.data_get(self.maintext_string)
    
    @property
    def deptexts_list(self):
        return [deptexts.dxf.text for deptexts in self.deptexts]
       
    @property    
    def shape(self):
        return Bar_shape(self.pline)

    @property
    def Type(self):
        return self.maintext_data['Type'] 
        
    @property
    def Grade(self):
        sign = self.maintext_data['Type'] 
        decoded_sign = rcbar_prop.decode_grade_sign(sign)
        return decoded_sign

    def Type_set(self, newType = None):
        self.data_set(newType = newType)

    @property
    def Size(self):
        return self.maintext_data['Size']

    def Size_set(self, newSize=None):
        self.data_set(newSize = newSize)

    @property
    def Mark(self):
        return self.maintext_data['Mark']

    def Mark_set(self,newMark=None):
        self.data_set(newMark = newMark)

    @property
    def Number(self):
        return self.maintext_data['Number']

    def Number_set(self,newNumber=None):
        self.data_set(newNumber = newNumber)
       
    @property
    def Total_Number(self):
        return self.maintext_data['Total_Number']

    @property
    def Length(self):
        return int(self.pline.length)

    @property
    def Total_Length(self):
        return self.Length * self.Total_Number

    @property
    def Mass(self):
        mass = rcbar_prop.mass_per_meter(self.Size) * self.Length / 1000.0
        mass = round(mass, 2)
        return mass
    
    @property
    def Total_Mass(self):
        mass = self.Mass * self.Number
        mass = round(mass, 2)
        return mass
        
    #----------------------------------------------
    
    def is_the_same_as(self, otherbar, tolerance=1.0):
        #print self.Mark, otherbar.Mark
        #---
        if not self.Size == otherbar.Size:
            #print 'zla srednica'
            return False
        if not self.Type == otherbar.Type:
            #print 'zly typ'
            return False
        if not abs(self.Length - otherbar.Length) < tolerance:
            #print 'zla dlugosc dla tolerancji', tolerance
            return False
        #---
        thisbar_shape_param = self.shape.shape_parameter
        otherbar_shape_param = otherbar.shape.shape_parameter
        otherbar_shape_param_rev = list(reversed(otherbar_shape_param))
        if len(thisbar_shape_param) == len(otherbar_shape_param):
            size = len(thisbar_shape_param)
            dif1 = [abs(thisbar_shape_param[i] - otherbar_shape_param[i]) for i in range(size)]
            dif2 = [abs(thisbar_shape_param[i] - otherbar_shape_param_rev[i]) for i in range(size)]
            dif1_check = all([value < tolerance for value in dif1])
            dif2_check = all([value < tolerance for value in dif2])
            #print dif1, dif2
            #print dif1_check, dif2_check
            if any([dif1_check, dif2_check]):
                #print 'bingoooooooooooo'
                return True
        return False
    
    def is_straight(self):
        if len(self.pline.get_coord_list()) == 2:
            return True
        else:
            return False

    #----------------------------------------------
        
    def __str__(self):
        return 'bar' + self.maintext_string + str(self.pline)

    def draw(self, scene):
        self.shape.draw(scene, color='red')
        space_mark = ''
        text = '%s%s[%s] L = %s'%(self.Type, self.Size, self.Mark, self.Length)
        scene.addMtext(space_mark + text, [0.0, 500.0], color='yellow', height = 200.0)
    
    #----------------------------------------------
    
    @property
    def schedule_record(self):
        return schedule_format.bar_record(self)
        
    #----------------------------------------------
    
    def get_test_dxf_pline_entity(self):
        #---geting random dxf_pline_entity from example dxf from 
        dwg = ezdxf.readfile(x_dxf_test_path.test_path)
        pline_entity_list = []
        for e in dwg.modelspace():
            if e.dxftype() == 'LWPOLYLINE' and e.dxf.layer == 'DS_CBAR':
                pline_entity_list.append(e)
        to_get = random.randint(0, len(pline_entity_list)-1)
        dxf_pline_entity = pline_entity_list[to_get]
        #--- writing to atribute
        self.dxf_pline_entity = dxf_pline_entity
        
if __name__ == "__main__":
    
    from environment import*
    #---
    DRAWING.open_file()
    #---
    SCANER.load_data_to_model()
    #---
    CONCRETE_MODEL.selftest()
    CONCRETE_MODEL.procces_data()
       
    print '=================================='

    bar = CONCRETE_MODEL.barlist[1]
    print bar.maintext_string
    print bar.Type
    print bar.Size
    print bar.Mark
    print bar.Total_Number
    
    bar.Mark_set('88')
    bar.Number_set(12)
    bar.Size_set(24)
    bar.data_set()
    bar.data_set(newNumber=4)
    bar.data_set(newMark='8')
    bar.data_set(newSize=12)
    
    bar = CONCRETE_MODEL.barlist[1]
    for bar in CONCRETE_MODEL.barlist:
        print bar.maintext_string
        bar._count_number_for_maintext()
