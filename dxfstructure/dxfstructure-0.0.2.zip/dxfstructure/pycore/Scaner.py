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

import uuid
import ezdxf
import os

from Bar import Bar
from Element import Element
from Drawing import Drawing
from ConcreteModel import ConcreteModel

from geo import Point, Line, Polyline, Rectangle,  pline_from_dxfpline
import text_syntax_element

class Scaner():
    def __init__(self):
        self.ConcreteModel = None
        self.Drawing = None
        self.pen = None
     
    #---------------------------------------------- 
        
    def asign_ConcreteModel(self, ConcreteModel):
        self.ConcreteModel = ConcreteModel

    def asign_Drawing(self, Drawing):
        self.Drawing = Drawing
        self.pen = self.Drawing.pen

    #----------------------------------------------
    
    def load_data_to_model(self):
        print '********* Loading data to model ***************'
        self.search_bars()
        self.search_maintext_for_bars()
        self.search_rangeplines_for_bars()
        #---
        self.search_elements()
        self.search_elements_text()
        self.assign_bar_to_element()
        #---
        self.clr_deps_if_request()
        self.assign_id_if_deplines()
        self.delete_deplines()
        #---
        self.search_deptext_for_bars()
        self.refresh_id()
        print '***********************************************'

    #----------------------------------------------
    
    def search_bars(self):
        print '---searching bars---'
        for i in self.Drawing.DS_BARS:
            self.ConcreteModel.add_bar(Bar(i))
        print '   %s bars found' %self.ConcreteModel.get_bar_number()
        print '   ....done'
    
    def search_maintext_for_bars(self):
        print '---searching maintext---'
        for bar in self.ConcreteModel.barlist:
            #--geting closest text from bar
            tdists = []
            for txt in self.Drawing.DS_CTEXTS:
                dxfinsert = txt.dxf.insert
                textp = Point([dxfinsert[0], dxfinsert[1]])
                txtdist = bar.pline.distance(textp)
                tdists.append(txtdist)
            mintdist = min(tdists)
            mintdistindex = tdists.index(mintdist)
            t_entity = self.Drawing.DS_CTEXTS[mintdistindex] #dxf text entity we looking for
            mintheigh = t_entity.dxf.height
            #---if found text is closest than it heigh from bar then assign it to bar
            if mintdist < mintheigh:
                bar.maintext = t_entity
        print '   ....done'
        
    def search_rangeplines_for_bars(self):
        print '---searching rangeplines---'
        for bar in self.ConcreteModel.barlist:
            for dxfpline in self.Drawing.DS_RANGEPLINES:
                pline = pline_from_dxfpline(dxfpline)
                bar_pline_intersection = pline.intersection(bar.pline)
                if bar_pline_intersection:
                    for circle in self.Drawing.DS_RANGECIRCELS:
                        circlecenter = Point(circle.dxf.center)
                        if bar_pline_intersection[0].intersection(circlecenter):
                            bar.rangepline = pline_from_dxfpline(dxfpline)  #!!!!!!!!!!
        print '   ....done'

    def search_elements(self):
        print '---searching elements---'
        for i in self.Drawing.DS_ELEMENT_FRAME:
            self.ConcreteModel.add_element(Element(i))
        print '   %s element found' %self.ConcreteModel.get_element_number()
        print '   ....done'

    def search_elements_text(self):
        print '---searching elements_name---'
        for element in self.ConcreteModel.elementlist:
            for txt in self.Drawing.DS_ELEMENT_TEXT:
                if element.rectangle.has_inside(Point(txt.dxf.insert)):
                    if text_syntax_element.has_correct_format(txt.dxf.text):
                        element.dxf_text_entity = txt
        print '   ....done'

    def assign_bar_to_element(self):
        print '---assign_bar_to_element---'
        for bar in self.ConcreteModel.barlist:
            for element in self.ConcreteModel.elementlist:
                if element.rectangle:
                    if element.rectangle.has_inside(bar.pline):
                        element.add_bar(bar)
                        bar.element = element
        #--creating freebar element
        if None in [bar.element for bar in  self.ConcreteModel.barlist]:
            freebar_element = Element()
            freebar_element.clear_data()
            freebar_element_name = 'FreeBars'
            freebar_element.name = freebar_element_name
            freebar_element.quantity = 1.0
            print '   (additional FreeBars element created)'
            self.ConcreteModel.add_element(freebar_element)
            for bar in self.ConcreteModel.barlist:
                if not bar.element:
                    freebar_element.add_bar(bar)
                    bar.element = freebar_element            
        print '   ....done'

    def clr_deps_if_request(self):
        print '---clr_deps_if_request---'
        for text in self.Drawing.DS_CTEXTS:
            if 'clr' in text.dxf.text:
                text.dxf.text = text.dxf.text.replace('clr', '')
                print 'bingo'
                self.Drawing.entity_id_set_random(text)
        print '   ....done'
        
    def assign_id_if_deplines(self):
        print '---assign_id_if_deplines---'
        for bar in self.ConcreteModel.barlist:
            #print bar.maintext
            if bar.maintext:
                maintext_id = self.Drawing.entity_id_get(bar.maintext)
                bar_maintext_point = list(bar.maintext.dxf.insert[:2])
                #print bar_maintext_point
                bar_maintext_point = Point(bar_maintext_point)
                for line in self.Drawing.DS_DEPLINES:
                    line_start_point = list(line.dxf.start[:2])
                    line_start_point = Point(line_start_point)
                    line_end_point = list(line.dxf.end[:2])
                    line_end_point = Point(line_end_point)
                    inter_start = bar_maintext_point.intersection(line_start_point)
                    inter_end = bar_maintext_point.intersection(line_end_point)
                    pick_point = None
                    if inter_start : pick_point = line_end_point
                    if inter_end : pick_point = line_start_point
                    if pick_point :
                        #print pick_point, 'bingo!!!!!!!!!!'
                        for text in self.Drawing.DS_CTEXTS:
                            ptext = list(text.dxf.insert[:2])
                            ptext = Point(ptext)
                            #print ptext, text.dxf.text
                            if pick_point.intersection(ptext):
                                #print text.dxf.text, self.Drawing.entity_id_get(text), '<<<<<<<<\this is picked'
                                self.Drawing.entity_id_set(text, maintext_id)
        print '   ....done'

    def delete_deplines(self):
        print '---delete_deplines---'
        to_delete_list = []
        for entity in self.pen.msp:
            if entity.dxf.layer == 'DS_DEPLINE':
                to_delete_list.append(entity) 
        self.pen.delete_entity(to_delete_list)
        print '   ....done'

    def search_deptext_for_bars(self):
        print '---search_deptext_for_bars---'
        maintexts = []
        for bar in self.ConcreteModel.barlist:
            if bar.maintext:
                maintexts.append(bar.maintext)
        #print maintexts
        for bar in self.ConcreteModel.barlist:
            if bar.maintext:
                bar_maintext_id = self.Drawing.entity_id_get(bar.maintext)
                #print 'looking for',bar_maintext_id , '+++++++++++++++++++++++++++'
                for text in self.Drawing.DS_CTEXTS:
                    #print self.Drawing.entity_id_get(text)
                    if self.Drawing.entity_id_get(text) == bar_maintext_id:
                        #print 'bingo'
                        if not text in maintexts:
                            #print 'found'
                            bar.deptexts.append(text)
        print '   ....done'

    def refresh_id(self):
        print '---refresch_id---'
        for bar in self.ConcreteModel.barlist:
            if bar.maintext:
                new_id = self.Drawing.entity_id_set_random(bar.maintext)
                for text in bar.deptexts:
                    self.Drawing.entity_id_set(text, new_id)
        print '   ....done'
    
    #----------------------------------------------

if __name__ == "__main__":
    
    from environment import*
    #---
    DRAWING.open_file()
    #---
    SCANER.load_data_to_model()
    #---
    #SCANER.pen.save()
    
    print CONCRETE_MODEL.elementlist[0]
    
    for element in CONCRETE_MODEL.elementlist:
        print element.maintext_string
        print element.name

    
    for bar in CONCRETE_MODEL.barlist:
        print bar.element
    