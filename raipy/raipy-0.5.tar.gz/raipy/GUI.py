# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 08:52:15 2017

@author: Yuki
"""
from PyQt5.QtGui import QFont,QIcon
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QToolBar,QAction,QMainWindow,QVBoxLayout,QWidget,QHBoxLayout,QTabWidget,QStatusBar,QTextEdit,QApplication,QWidgetAction,QMenuBar,QMenu,QTextBrowser

from raipy.Constant import *
from raipy.Controller import *
from raipy.FileManager import *
from raipy.GraphManager import *
from raipy.LCD_Display import *
from raipy.MyPyqtGraph import *
from raipy.Time import *
from raipy.Help import helpText
from raipy.Example import ExampleMenu

ICON='Icons//logo.png' #the relative path of the logo image

class MyMenuBar(QMenuBar):
    '''自作Menubar 状態を持ちその状態によって押せるボタンが変化する その状態としてはQMainWindowの状態を参照する QMainWindowのstateSignalと繋ぐことで状態をupdate'''
    def __init__(self,ref):
        super().__init__()
        self.loadAction=QAction('Load a program', self)
        self.loadAction.setShortcut('Ctrl+L')
        self.tempAction = QAction('Output a template', self)
        self.tempAction.setShortcut('Ctrl+T')
        self.explaAction = QAction('About this program', self)
        self.explaAction.setShortcut('Ctrl+H')
        
        self.fileMenu =self.addMenu('File')
        self.fileMenu.addAction(self.loadAction)
        self.fileMenu.addAction(self.tempAction)
        
        helpMenu=self.addMenu('Help')
        helpMenu.addAction(self.explaAction)
        self.exampleMenu=ExampleMenu('Examples',self)
        helpMenu.addMenu(self.exampleMenu)
        
        self.setState(ref.state)
        ref.stateSignal.connect(self.setState)
        
    def setState(self,end):
        '''状態の遷移はこの関数を通して行われる'''
        if end==RUNNING:
            self.loadAction.setEnabled(False)
        else:
            self.loadAction.setEnabled(True)
            
class MyToolBar(QToolBar):
    '''自作Toolbar 状態を持ちその状態によって押せるボタンが変化する その状態としてはQMainWindowの状態を参照する QMainWindowのstateSignalと繋ぐことで状態をupdate'''
    def __init__(self,ref):
        super().__init__()
        self.exeAction=QAction('Run', self)
        self.stopAction = QAction('Stop', self)
        self.reloadAction = QAction('Reload', self)
        self.addAction(self.exeAction)
        self.addAction(self.stopAction)
        self.addAction(self.reloadAction)
        
        self.setState(ref.state)
        ref.stateSignal.connect(self.setState)
        
    def setState(self,end):
        '''状態の遷移はこの関数を通して行われる'''
        if end==INITIAL:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(False)
            self.reloadAction.setEnabled(False)
        elif end==READY:
            self.exeAction.setEnabled(True)
            self.stopAction.setEnabled(False)
            self.reloadAction.setEnabled(True)
        elif end==MISTAKE:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(False)
            self.reloadAction.setEnabled(True)
        elif end==RUNNING:
            self.exeAction.setEnabled(False)
            self.stopAction.setEnabled(True)
            self.reloadAction.setEnabled(False)
            
class GUIWindow(QMainWindow):
    stateSignal=pyqtSignal(int)
    def __init__(self): 
        super().__init__()
        self.state=INITIAL
        self.setWindowIcon(QIcon('.\\icon\\python_logo.png'))
        self.initUI()
        self.setState(INITIAL)
        self.params={} #programThreadの生成時に渡してcontrollerによる制御を可能にする
        
    def initUI(self):   
        #add Menubar
        menubar=MyMenuBar(self)
        menubar.explaAction.triggered.connect(self.showExplanation)
        self.setMenuBar(menubar)
            
        #Toolbarを付ける
        toolbar=MyToolBar(self)
        toolbar.exeAction.triggered.connect(self.exePressed)
        toolbar.stopAction.triggered.connect(self.stopPressed)
        self.addToolBar(toolbar)
        
        
        #tab1
        self.pathbox=MyPathBox()
        self.pathbox.importSig.connect(self.fileAppointed)
        menubar.exampleMenu.setFileManager(self.pathbox)
        menubar.loadAction.triggered.connect(self.pathbox.showDialog)
        menubar.tempAction.triggered.connect(self.pathbox.tempPressed)
        toolbar.reloadAction.triggered.connect(self.pathbox.rePressed)
        
        self.gm=MyGraphManager('Graphs',self.pathbox.get_output_labels,self.pathbox.get_output_units,\
                               self.pathbox.outputLabelChangeSig,self.pathbox.outputUnitChangeSig,self.pathbox.graphSettingSig,self)
        vbox=QVBoxLayout()
        vbox.addWidget(self.pathbox)
        vbox.addWidget(self.gm)
        setTab=QWidget()
        setTab.setLayout(vbox)
        
        #tab2
        self.lcdContainer=MyLCDContainer(self.pathbox.get_output_labels,self.pathbox.get_output_units,\
                                         self.pathbox.outputLabelChangeSig,self.pathbox.outputUnitChangeSig,self)
        self.time=MyTimeBox()
        #サイズ調整
        sizePolicyTime=self.time.sizePolicy()
        sizePolicyLcd=self.lcdContainer.sizePolicy()
        sizePolicyTime.setHorizontalStretch(1)
        sizePolicyLcd.setHorizontalStretch(1)
        self.time.setSizePolicy(sizePolicyTime)
        self.lcdContainer.setSizePolicy(sizePolicyLcd)
        
        hbox=QHBoxLayout()
        hbox.addWidget(self.lcdContainer)
        hbox.addWidget(self.time)
        displayTab=QWidget()
        displayTab.setLayout(hbox)
        
        #tab3
        self.sContainer=MyContainer(self.pathbox.getSliders,self.pathbox.sliderChangeSig,MySlider,self)
        self.bContainer=MyContainer(self.pathbox.getBools,self.pathbox.boolChangeSig,MyBool,self)
        self.dContainer=MyContainer(self.pathbox.getDials,self.pathbox.dialChangeSig,MyDial,self)
        self.fContainer=MyContainer(self.pathbox.getFloats,self.pathbox.floatChangeSig,MyFloat,self)
        self.sContainer.valueChanged.connect(self.updateParam)
        self.bContainer.valueChanged.connect(self.updateParam)
        self.dContainer.valueChanged.connect(self.updateParam)
        self.fContainer.valueChanged.connect(self.updateParam)
        hbox2=QHBoxLayout()
        hbox2.addWidget(self.sContainer)
        hbox2.addWidget(self.bContainer)
        hbox2.addWidget(self.dContainer)
        hbox2.addWidget(self.fContainer)
        controlTab=QWidget()
        controlTab.setLayout(hbox2)
        
        #tabをまとめる
        self.qTab=QTabWidget()
        self.qTab.setStyleSheet('QTabWidget::tab-bar{alignment: center;}')  #ツールバーのボタンとの押し間違えを防ぐために中央に配置
        self.qTab.addTab(setTab,'setting')
        self.qTab.addTab(displayTab,'display')
        self.qTab.addTab(controlTab,'control')
        self.setCentralWidget(self.qTab)
        
        #status barを付ける
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)
        
        #windowを描画
        self.setGeometry(10, 60, 960,900)
        self.setWindowTitle(' raipy')
        import raipy
        import os
        path=os.path.dirname(os.path.abspath(raipy.__file__))+'\\'+ICON
        self.setWindowIcon(QIcon(path))
        
        self.show()
        
    def exePressed(self):
        if self.state==READY:
            if self.pathbox.showDataDialog():
                self.gm.initData()
                self.initParams(self.sContainer.getInits(),self.bContainer.getInits(),self.dContainer.getInits(),self.fContainer.getInits())
                self.thread=self.pathbox.program.programThread(self.params)
                self.thread.outputSignal.connect(self.lcdContainer.update_data)
                self.thread.finished.connect(self.program_exit)  #stopボタンが押されないまま全ての処理が終わった場合のため
                self.thread.outputSignal.connect(self.gm.updateData)
                self.thread.outputSignal.connect(self.pathbox.write_data)
                self.thread.start()
                self.time.startTimer()
                self.setState(RUNNING)
                self.qTab.setCurrentIndex(1)
            
    def stopPressed(self):
        if self.state==RUNNING:
            self.thread.terminate() #stopでの停止と全部の処理の終了での停止をまとめて処理するため ここでは状態を遷移しない
        
    def showExplanation(self):
        try:
            self.text.showNormal()
        except:
            self.text=QTextBrowser()
            self.text.setOpenExternalLinks(True)
            self.text.setGeometry(20, 120, 800, 700)
            self.text.setWindowTitle('Help')
            self.text.setFont(QFont('TimesNewRoman',12))
            self.text.setHtml(helpText)
            self.text.setReadOnly(True)
            self.text.show()
            
    def demoPressed(self):
        pass
        
    def initParams(self,*mydicts):
        self.params={}
        for mydict in mydicts:
            for key in mydict:
                self.params[key]=mydict[key]
        print('----------------control parameters---------------------\n')
        print(self.params)
                
    def updateParam(self,mydict):
        for key in mydict:
            self.params[key]=mydict[key]
            
    def fileAppointed(self,success):
        #switch the state based on whether import succeeded or not
        if success:
            self.setState(READY)
        else:
            self.setState(MISTAKE)
        
#    @classmethod
#    def instSearch(cls,mylist):
#        #指定された測定器が繋がっているかチェックする
#        #currently not implemented.Might be removed.
#        return True
        
    def program_exit(self):
        self.pathbox.data_file_close()
        self.time.stopTimer()
        self.setState(READY)
        
    def setState(self,state):
        '''状態は必ずこの関数を用いて遷移させる'''
        self.state=state
        if self.state==INITIAL:
            self.status_bar.showMessage('choose file')
        elif self.state==READY:
            self.status_bar.showMessage('ready to start the program')
        elif self.state==MISTAKE:
            self.status_bar.showMessage('your program has a mistake at least.see the prompt window')
        elif self.state==RUNNING:
            self.status_bar.showMessage('program is running')
        self.stateSignal.emit(self.state)
        
    def closeEvent(self,event):
        #to be called when the window is closed
        self.pathbox.clean_up()
        

#メイン　
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex=GUIWindow()
    sys.exit(app.exec_())