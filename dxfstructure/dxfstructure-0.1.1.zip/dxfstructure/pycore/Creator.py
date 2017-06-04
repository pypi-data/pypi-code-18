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

from Drawing import Drawing
import layer_system

class Creator():
    def __init__(self):
        self.Drawing = None
        self.pen = None
    #----------------------------------------------

    def asign_Drawing(self, Drawing):
        self.Drawing = Drawing
        self.pen = self.Drawing.pen

    #-------------inject DS ---------------------------------
    def inject_DS_system(self):
        self._create_layer_system()

    def _create_layer_system(self):
        for layername in layer_system.layer_name_list:
            #---
            color = layer_system.color_for_layer(layername)
            width = layer_system.width_for_layer(layername)
            lintype = layer_system.linetype_for_layer(layername)
            line_weight = layer_system.width_for_layer(layername)
            #----
            self.pen.layer_add(name=layername, linetype=lintype, color=color, line_weight = line_weight)
        
    #----------------------------------------------

    def DoCommand(self, command): # under construction ...
        if command == 'draw_xxx':
            self._draw_xxx()

    def _draw_xxx(self): # under construction ...
        print  'draw_xxx'
        self.Drawing.pen.set_origin([222.0,200.0])
        self.Drawing.pen.addLine([0.0, 0.0], [300.0, 400.0], 'blue')

# Test if main
if __name__ == "__main__":
    from environment import*
    DRAWING.open_file()
    #---
    CREATOR._draw_xxx()
    CREATOR.DoCommand('draw_xxx')
    CREATOR.Drawing.save()