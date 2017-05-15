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

from geo import Point
import schedule_format

from tabulate import tabulate

class Schedule():
    def __init__(self):
        self.ConcreteModel = None
        self.Drawing = None
        self.pen = None
        self.layer = 'DS_SCHEDULE'

    #----------------------------------------------
        
    def asign_ConcreteModel(self, ConcreteModel):
        self.ConcreteModel = ConcreteModel

    def asign_Drawing(self, Drawing):
        self.Drawing = Drawing
        self.pen = self.Drawing.pen
    
    #----------------------------------------------    
    
    @property
    def main_schedule_text(self):
        header = schedule_format.header()
        records = self.ConcreteModel.schedule_record
        #---
        schedule = header + records
        main_schedule_text = tabulate(schedule, numalign="right")  
        main_schedule_text += "\nCALKOWITA MASA DLA RYSUNKU : %s [kg]"%(self.ConcreteModel.Mass)  
        #main_schedule_text += "\nTOTAL MASS FOR DRAWING : %s [kg]"%(self.ConcreteModel.Mass)  
        return str(main_schedule_text)

    #----------------------------------------------
        
    def draw_schedule_in_drawing (self):
        print '****** drawing bar schedule in drawing ************'
        self.pen.set_origin()
        self.delete_existing_schedule_from_drawing()
        #---
        self.pen.set_current_layer(self.layer)
        #---
        inserpoint = [0.0, 0.0]
        #---main schedule
        main_schedule_text = self.main_schedule_text
        main_schedule_text = '{\Fcdm;%s}'%main_schedule_text #defining font
        self.pen.addMtext(main_schedule_text, [0.0, 0.0], height = 150, color = 'yellow')
        #---shape schedule
        inserpoint = [25000.0, 0.0]
        self.pen.set_origin(inserpoint)
        for bar in self.ConcreteModel.unicat_bars_sorted_numered:
            if bar.maintext:
                if not bar.is_straight():
                    bar.draw(self.pen)
                    self.pen.move_origin(0, -(bar.shape.sizexy[1] + 1100))
        p1 = [-200.0, 200.0]
        p2 = [2800.0, self.pen.origin[1]]
        self.pen.set_origin(inserpoint)
        #self.pen.addText('main schedule', [0.0, 400], height = 100, color = 'yellow')
        print '   ...done'
        print '***************************************************'    
        

        '''
        out_text = 'Element %s' %self.name
        out_text += '\n'
        out_text += tabulate(bar_records, numalign="right")
        return out_text
        '''
    
    def delete_existing_schedule_from_drawing(self):
        to_delete_list = []
        for entity in self.pen.msp:
            if entity.dxf.layer == self.layer:
                to_delete_list.append(entity) 
        self.pen.delete_entity(to_delete_list)

if __name__ == "__main__":
    #---
    from environment import*
    DRAWING.open_file()
    SCANER.load_data_to_model()
    
    CONCRETE_MODEL.selftest()
    
    
    SCHEDULE.draw_schedule_in_drawing()
    
    SCHEDULE.pen.save()