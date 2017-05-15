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


layers =    {   'DS_CBAR' :     [133, 30, 'CONTINUOUS'],
                'DS_CTEXT' :    ['yellow', 20, 'CONTINUOUS'],
                'DS_DEPLINE' :  [46, 15,'CONTINUOUS'],
                'DS_ELEMENT' :  [234, 20, 'CONTINUOUS'],
                'DS_RANGE' :    [92, 18, 'CONTINUOUS'],
                'DS_SCHEDULE' : ['yellow', 20, 'CONTINUOUS'],
                'DS_MARKS' :    [253, 18, 'CONTINUOUS'],
                'DS_TMPCHECK' : [186, 15, 'CONTINUOUS']
            }

layer_name_list = layers.keys()

def color_for_layer(layer_name):
    return layers[layer_name][0]
    
def width_for_layer(layer_name):
    return layers[layer_name][1]
    
def linetype_for_layer(layer_name):
    return layers[layer_name][2]


for i in layers:
    print i 
        
        
        
if __name__ == "__main__":
    
    pass
    #T1 = '10#12-[5]'
    #pT1 = re.compile('\A\s*(\d*)#(\d+)-\[(\d+)\]\s*\Z')
    #print pT1.search(T1).group()
    
    #T2 = '5#12-[5]-200DG'
    #pT2 = re.compile('\A\s*(\d*)#(\d+)-\[(\d+)\]-(\d*)(\D*)\s*\Z')
    #print pT2.search(T2).group()
    #print pT2.sub(r'\1#\2-[\3]-\4\5', T2)

    #NUMBER = 50
    #MARK = 10
    #print pT2.sub(r'%s#\2-[%s]-\4\5'%(NUMBER, MARK), T2)        
    
    #print 't333333'
    #T3 = '5#12-[5]-200DG'
    #T3 = '5#12-[5]'
    #pT3 = re.compile('\A\s*(\d*)#(\d+)-\[(\d+)\](-*)(\d*)(\D*)\s*\Z')
    #print pT3.findall(T3)
    #print pT3.search(T3)
    
    #text = '5#12-[5]-200DG'
    #print has_correct_format(text)
    #print data_get(text)