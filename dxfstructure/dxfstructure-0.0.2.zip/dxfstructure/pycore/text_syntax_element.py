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

import re

#-----EL. Bk1 x 2------

re_text = re.compile('\s*Element (.*) x (\d*)\s*')
                  
def has_correct_format(text):
    if re_text.search(text):
        return True
    else:
        return False

def data_get(text):
    if has_correct_format(text):
        data = re_text.findall(text)[0]
        #---
        Name = data[0] 
        Number = float(data[1])
        #---
        return { 'Number':Number, 'Name':Name }
    else:
        return None
        
if __name__ == "__main__":
    test_text = 'Element Bk-5 x 5'
    print has_correct_format(test_text)
    print data_get(test_text)