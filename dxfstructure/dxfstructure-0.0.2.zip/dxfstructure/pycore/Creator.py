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

    #----------------------------------------------

    def create_layer_system(self):
        for layername in layer_system.layer_name_list:
            #---
            color = layer_system.color_for_layer(layername)
            width = layer_system.width_for_layer(layername)
            lintype = layer_system.linetype_for_layer(layername)
            line_weight = layer_system.width_for_layer(layername)
            #----
            self.pen.layer_add(name=layername, linetype=lintype, color=color, line_weight = line_weight)
        

    #----------------------------------------------

    def DoCommand(self, command):
        if command == 'draw_xxx':
            self._draw_xxx()

    #----------------------------------------------

    def _draw_xxx(self):
        print  'draw_xxx'
        self.Drawing.pen.set_origin([222.0,200.0])
        self.Drawing.pen.addLine([0.0, 0.0], [300.0, 400.0], 'blue')

if __name__ == "__main__":
    from environment import*
    DRAWING.open_file()
    #---
    CREATOR._draw_xxx()
    CREATOR.DoCommand('draw_xxx')
    CREATOR.Drawing.save()
