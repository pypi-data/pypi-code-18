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
from ConcreteModel import ConcreteModel
from Drawing import Drawing
from Scaner import Scaner

#from EzdxfPen2D import EzdxfPen2D

class Checker():
    def __init__(self):
        self.ConcreteModel = None
        self.Drawing = None
        self.pen = None
        self.layer = 'DS_TMPCHECK'
        
    #----------------------------------------------
    
    def asign_ConcreteModel(self, ConcreteModel):
        self.ConcreteModel = ConcreteModel

    def asign_Drawing(self, Drawing):
        self.Drawing = Drawing
        self.pen = self.Drawing.pen
        
    #----------------------------------------------
    
    def check_all(self, dosave = False):
        print '********* Checking all data ***************'
        self.delete_all_marks()
        #---
        isCorrect = []
        isCorrect.append(self.bar_with_no_text())
        isCorrect.append(self.text_with_no_bar())
        if dosave:
            self.pen.save()
        #---
        check_result = all(isCorrect)
        if check_result:
            print '>>>any problem detected<<<'

        else:
            print '>>>!!some problem detected!!<<<'
        print '*******************************************'
        return check_result
            
    #----------------------------------------------
    
    def bar_with_no_text(self):
        isCorrect = True
        print '---bar_with_no_text---'
        for bar in self.ConcreteModel.barlist:
            if not bar.maintext:
                p = bar.pline.get_coord_list()[0]
                self.pen.set_current_layer(self.layer)
                self.pen.addText('no text for bar!!!', p, height=200, color = 'red')
                self.pen.addLine([0.0, 0.0], p, color = 'red')
                print '  found at %s' %p
                isCorrect = False
        print '   ...done'
        return isCorrect

    def text_with_no_bar(self):
        isCorrect = True
        print '---text_with_no_ba---r'
        texts_in_bars = [bar.maintext for bar in self.ConcreteModel.barlist]
        for text in self.Drawing.DS_CTEXTS:
            if not text in texts_in_bars:
                p = list(text.dxf.insert[:2])
                self.pen.set_current_layer(self.layer)
                self.pen.addText('no bar for text!!!', p, height=200, color = 'red')
                self.pen.addLine([0.0, 0.0], p, color = 'red')
                print '  found at %s' %p
                isCorrect = False
        print '   ...done'
        return isCorrect
        
    def text_with_wrong_format(self):
        pass   

    def text_not_linked(self):
        pass
        
    #----------------------------------------------
    
    def show_depenance(self):
        print '---show_depenance---'
        self.pen.set_current_layer(self.layer)
        self.pen.set_origin()
        for bar in self.ConcreteModel.barlist:
            if bar.maintext:
                maintext_point = list(bar.maintext.dxf.insert[:2])
                for text in bar.deptexts:
                    text_point = list(text.dxf.insert[:2])
                    self.pen.addLine(maintext_point, text_point, color = 'blue')
        print '   ...done'
                
    #----------------------------------------------
    
    def delete_all_marks(self):
        print '---deleting all warnings marks---'
        to_delete_list = []
        for entity in self.pen.msp:
            if entity.dxf.layer == 'DS_TMPCHECK':
                to_delete_list.append(entity) 
        self.pen.delete_entity(to_delete_list)
        print '   ...done'

if __name__ == "__main__":
    #---
    SCANER = Scaner()
    #---
    DRAWING = Drawing()
    DRAWING.open_file()
    CONCRETE_MODEL = ConcreteModel()
    #---
    SCANER.asign_Drawing(DRAWING)
    SCANER.asign_ConcreteModel(CONCRETE_MODEL)
    #---
    SCANER.search_bars()
    SCANER.search_maintext_for_bars()
    SCANER.search_rangeplines_for_bars()
    SCANER.search_elements()
    SCANER.assign_bar_to_element()
    
    CHECKER = Checker()
    CHECKER.asign_ConcreteModel(CONCRETE_MODEL)
    CHECKER.asign_Drawing(DRAWING)
    
    CHECKER.delete_all_marks()
    
    print CHECKER.check_all()
    
    CHECKER.pen.save()

    
    