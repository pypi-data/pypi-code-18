#!/usr/bin/python

#   Copyright (c) 2017, Pan Labs (panorbit.in).  
#   This file is licensed under the MIT License.
#   See the LICENSE file.

import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import random
import json


#this function prints data to txt file
#it takes data and ProjectName(name of file) as input
#gets fileName.txt in output folder
def PrintIt(data,ProjectName):

    if ProjectName:
        fileName='.'.join([ProjectName,'txt'])
        path='/'.join(['output',fileName])
    else:
        fileName='.'.join(['output','txt'])
        path='/'.join(['output',fileName])

    f=open(fileName,'a')
    f.write(data)
    f.close()



#this functions prints data into json file (json format)
class Json():
    def __init__(self):
        self.PresentURL=''
        self.data=''
        self.ProjectName=''
        self.Data={}

    def jsonData(self):

        if self.PresentURL in self.Data:
            self.Data[self.PresentURL]+=' '+self.data
        else:
            self.Data[self.PresentURL]=self.data
        json_encoded=json.dumps(self.Data)

        if self.ProjectName:
            fileName='.'.join([self.ProjectName,'json'])
            path='/'.join(['output',fileName])
        else:
            fileName='.'.join(['output','json'])
            path='/'.join(['output',fileName])

        f=open(fileName,'w')
        f.write(json_encoded)
        f.close()
