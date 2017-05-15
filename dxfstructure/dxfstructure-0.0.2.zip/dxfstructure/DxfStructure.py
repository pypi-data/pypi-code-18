'''
--------------------------------------------------------------------------
Copyright (C) 2015-2017 Lukasz Laba <lukaszlab@o2.pl>

File version 0.7 date 2017-03-06
This file is part of Struthon.
Struthon is a range of free open source structural engineering design 
Python applications.
http://struthon.org/

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import sys
import os
import uuid

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer

from qtui.mainwindow_ui import Ui_MainWindow

import ezdxf

from pycore.environment import DRAWING, CONCRETE_MODEL, SCANER, CREATOR, CHECKER, SCHEDULE

APP_PATH = os.path.dirname(os.path.abspath(__file__))

_appname = 'DxfStructure'
_version = '0.0.2'

class MAINWINDOW(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #---Button clicked events 
        self.ui.pushButton_Check.clicked.connect(Check)
        self.ui.pushButton_Check_and_save.clicked.connect(Check_and_save)
        self.ui.pushButton_Show_dep_and_save.clicked.connect(Show_depndence_and_save)
        self.ui.pushButton_Process.clicked.connect(Process_data)
        self.ui.pushButton_Process_renum.clicked.connect(Process_data_with_renumerate)
        self.ui.pushButton_Process_renum_schedules.clicked.connect(Process_data_with_enumerate_and_schedules)
        #---MenuBar events
        self.ui.actionLoad_dxf.triggered.connect(Open)

    #--method for sys.stdout 
    def write(self, text):
        if text == '\n': return 0
        myapp.ui.textBrowser.append(text)
        
#---------------------------------------------------------
#----------------------Ui event action--------------------
#---------------------------------------------------------
def Open(test=False):
    filename = None
    if not test:
        directory = ''
        if DRAWING.filepath: directory = os.path.dirname(DRAWING.filepath)
        filename = QtGui.QFileDialog.getOpenFileName( caption = 'Open dxf', directory = directory, filter = "DXF (*.dxf)")
        filename = str(filename)
        #---
        progress(30)
    clear_model_data()
    DRAWING.open_file(filename)
    progress(60)
    SCANER.load_data_to_model()
    myapp.setWindowTitle(_appname + ' ' + _version + ' - ' + os.path.basename(DRAWING.filepath))
    progress(100)

def Check():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CHECKER.check_all()
    #--
    progress(100)

def Check_and_save():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CHECKER.check_all()
    save()
    #--
    progress(100)

def Show_depndence_and_save():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CHECKER.show_depenance()
    save()
    #--
    progress(100)

def Process_data():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CONCRETE_MODEL.selftest()
    CONCRETE_MODEL.procces_data()
    save()
    #--
    progress(100)

def Process_data_with_renumerate():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CONCRETE_MODEL.selftest()
    CONCRETE_MODEL.procces_data()
    CONCRETE_MODEL.renumerate()
    save()
    #--
    progress(100)

def Process_data_with_enumerate_and_schedules():
    myapp.ui.textBrowser.clear()
    if not DRAWING.filepath: 
        no_data_massage()
        return 0
    #--
    progress(50)
    #---
    reload_file()
    CONCRETE_MODEL.selftest()
    CONCRETE_MODEL.procces_data()
    CONCRETE_MODEL.renumerate()
    SCHEDULE.draw_schedule_in_drawing()
    save()
    #--
    progress(100)
#---------------------------------------------------------
#---------------------------------------------------------

def reload_file():
    clear_model_data()
    #---
    DRAWING.reload_file()
    SCANER.load_data_to_model()
    
def clear_model_data():
    DRAWING.create_data_fields()
    CONCRETE_MODEL.create_data_fields()

def save():
    DRAWING.save()

def no_data_massage():
    QtGui.QMessageBox.information(None, 'Info', 'Please open dxf file first')

def progress(value=0):
        if value:
            myapp.ui.progressBar.setVisible(True)
        myapp.ui.progressBar.setValue(value - 1)
        myapp.ui.progressBar.setValue(value)
        if value == 100:
            myapp.ui.progressBar.setVisible(False)
            myapp.ui.progressBar.setValue(0)
#---------------------------------------------------------
#---------------------------------------------------------


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MAINWINDOW()
    #--
    myapp.setWindowTitle(_appname + ' ' + _version)
    myapp.ui.progressBar.setVisible(False)
    #--
    sys.stdout = myapp
    sys.stderr = myapp
    #--
    Open(True)
    #--
    myapp.show()
    sys.exit(app.exec_())