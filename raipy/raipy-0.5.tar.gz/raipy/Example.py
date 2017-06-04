# -*- coding: utf-8 -*-
"""
Created on Sat May 13 21:48:22 2017

@author: Yuki
"""
from PyQt5.QtWidgets import QVBoxLayout,QWidget,QHBoxLayout,QTabWidget,QStatusBar,QTextEdit,QApplication,QPushButton,QMenu,QAction
from PyQt5.QtCore import pyqtSignal
EXAMPLE='Examples' #the folder exists in the same folder with __init__.py and contains samples

class MyAction(QAction):
    actionName=pyqtSignal(str)
    def __init__(self,*args):
        super().__init__(*args)
        self.triggered.connect(self.myEmit)
        
    def myEmit(self):
        self.actionName.emit(self.text())

class ExampleMenu(QMenu):
    '''show example programs in Example folder'''
    def __init__(self,*args):
        super().__init__(*args)
        import raipy
        import os
        folder=os.path.dirname(os.path.abspath(raipy.__file__))+'\\'+EXAMPLE
        files=os.listdir(folder)
        pyfiles=[file for file in files if ('.py' in file)]
        self.setList(pyfiles)
        
    def setList(self,files):
        #append file names to itself and connect signals
        for file in files:
            action=MyAction(file,self)
            self.addAction(action)
            action.actionName.connect(self.showExample)
            
    def setFileManager(self,manager):
        self.manager=manager
            
    def showExample(self,file):
        self.example=ExampleWidget(file,self.manager)
        self.example.show()
        

class ExampleWidget(QWidget):
    load=pyqtSignal(str)
    export=pyqtSignal(str)
    def __init__(self,file,manager):
        super().__init__()
        exe=QPushButton('Load')
        export=QPushButton('Export')
        exe.pressed.connect(self.emitLoad)
        export.pressed.connect(self.emitExport)
        self.load.connect(manager.importFile)
        self.export.connect(manager.copyFile)
        buttons=QHBoxLayout()
        buttons.addWidget(exe)
        buttons.addWidget(export)
        buttons.addStretch(1)
        
        self.text=QTextEdit()
        
        vbox=QVBoxLayout()
        vbox.addLayout(buttons)
        vbox.addWidget(self.text)
        
        self.setLayout(vbox)
        self.setText(file)
        self.text.setReadOnly(True)
        self.setGeometry(500, 60, 960,900)
        
    def setText(self,file):
        #show a file in EXAMPLE folder 
        import raipy
        import os
        folder=os.path.dirname(os.path.abspath(raipy.__file__))+'\\'+EXAMPLE
        self.path=folder+'\\'+file
        import codecs
        f=codecs.open(self.path,'r','utf-8')
        text=f.read()
        self.text.setText(text)
        
    def emitLoad(self):
        self.load.emit(self.path)
        
    def emitExport(self):
        self.export.emit(self.path)
        
#メイン　
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ex=ExampleWidget()
    ex.show()
    import raipy
    import os
    root=os.path.dirname(os.path.abspath(raipy.__file__))
    path=root+'\\Examples\\Demo.py'
    print(path)
    ex.setText(root+'\\Examples\\Demo.py')
    ll=ExampleList()
    print(ll.getExamples())
    sys.exit(app.exec_())