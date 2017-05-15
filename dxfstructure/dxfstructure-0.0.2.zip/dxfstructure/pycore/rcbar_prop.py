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

import math

steel_density = 7850.0 # [kg/m]

def mass_per_meter(bar_diameter = 12): # bar_diameter [mm]
    bar_diameter = float(bar_diameter)
    area = math.pi * (bar_diameter / 1000.0)**2 / 4.0
    mass = area * steel_density
    mass = round(mass, 3)
    return mass
    
grade_signs = {'#' : 'B500A'} 
    
def decode_grade_sign(sign):
    if sign in grade_signs.keys():
        return grade_signs[sign]
    else:
        return str(sign)
        
if __name__ == "__main__":
    pass
    print mass_per_meter(12.0)
    print decode_grade_sign('#')
    print decode_grade_sign('3')