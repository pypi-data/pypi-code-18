# -*- coding: utf-8 -*-
import PyQt5.QtCore
from PyQt5.QtGui import QColor
import time
import numpy as np
import raipy.UserClassBase as UserClassBase
from datetime import datetime

HALT='Halt'
T_I='interval(s)'
NUM=7

LINES_U=[['Line_'+str(i),'V'] for i in range(NUM)]
LINES=['Line_'+str(i) for i in range(NUM)]
COLORS=[QColor(255,0,0),QColor(255,255,0),QColor(128,255,0),QColor(0,255,255),QColor(0,128,255),QColor(255,0,128),QColor(255,0,255)]
BOOLS=[['Noise_'+str(i),False] for i in range(NUM)]
SLIDERS=[['Amplitude_'+str(i),0,100,50] for i in range(NUM)]
DIALS=[['Phase_'+str(i),0,359,i] for i in range(NUM)]
FLOATS=[['Offset_'+str(i),i] for i in range(NUM)]

class programThread(PyQt5.QtCore.QThread):
    outputSignal=PyQt5.QtCore.pyqtSignal(dict)   #You must emit all graph data at onece
    def __init__(self,params):
        super().__init__()
        self.params=params
    def run(self):
        ###The main body of your program
        ###example: Call self.lcdSignal.emit({'Temperature':1,'Voltage':2}) if you want to display 1 on 'Temperature' display and 2 on 'Voltage' display.
        print('thread started')
        timeOrigin=datetime.now()
        for i in range(1000000):
            time.sleep(self.params[T_I])
            if not self.params[HALT]:
                t=(datetime.now()-timeOrigin).total_seconds()
                values=[]
                for j in range(NUM):
                    value=self.params[SLIDERS[j][0]]*np.cos(t+self.params[DIALS[j][0]]*np.pi/180)+self.params[FLOATS[j][0]]
                    if self.params[BOOLS[j][0]]:
                        value=value+self.params[SLIDERS[j][0]]*np.random.rand()
                    values.append(value)
                outputs={'Time':t}
                for label,value in zip(LINES,values):
                    outputs[label]=value
                self.outputSignal.emit(outputs)

class Output(UserClassBase.OutputBase):
    ###Write the labels of your measured values with dimensions
    #format：[[label],[unit]] example:graph_outputs=[['Temperature','K'],['Voltage','V']]
    outputs=[['Time','s']]+LINES_U
    
    ###Write the settings you want to show up in Graphs in advance
    #format:[[x axis label,[y axis label 1,y axis label 2],[color 1,color 2]],[settings for the second graph]] example：[['Time',['Voltage','Current'],[QColor(255,255,0),QColor(0,255,255)]]]
    graph_settings=[['Time',LINES,COLORS]]
    
class Control(UserClassBase.ControlBase):
    ###Write your control parameters with initial values
    bools=[[HALT,False]]+BOOLS    #format:bools=[['label',bool]] example：bools=[['flag_A',True],['flag_B',False]]
    sliders=SLIDERS #format：sliders=[['label',minimum(int)、maximum（int）、initial value（int）]] example：sliders=[['slider_A',0,10,5],['slider_B',0,200,0]]
    dials=DIALS    #same on 
    floats=[[T_I,0.05]]+FLOATS   #format：floats=[['label',initial value（float）]] example：floats=[['param_PI',3.14159265],[param_E,2.71828]]