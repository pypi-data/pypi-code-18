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

test_path = os.path.dirname(os.path.abspath(__file__))
test_path = os.path.dirname(test_path)
test_path = os.path.join(test_path, 'dxftest/test.dxf')