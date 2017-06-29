import clr
import sys, os

dir_path = os.path.dirname(os.path.abspath(__file__))

files = os.listdir(dir_path)

for file in files:
    if ".dll" in file:
        print('QuantApp Linking CLR dll: ' + dir_path + os.path.sep + file)        
        clr.AddReference(dir_path + os.path.sep + file)

