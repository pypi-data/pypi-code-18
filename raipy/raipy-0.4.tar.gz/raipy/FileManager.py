# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 09:11:01 2017

@author: Yuki
"""
import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QLabel,QApplication,QFileDialog

import raipy.UserClassBase as UserClassBase

class MyPathBox(QWidget):
    '''ファイルパスを表示するためのクラス　読み取りのみ可'''
    importSig=pyqtSignal(bool) #emit when import succeed
    graphSettingSig=pyqtSignal(list)
    outputLabelChangeSig=pyqtSignal(list)
    outputUnitChangeSig=pyqtSignal(list)
    boolChangeSig=pyqtSignal(list)
    sliderChangeSig=pyqtSignal(list)
    dialChangeSig=pyqtSignal(list)
    floatChangeSig=pyqtSignal(list)
    def __init__(self):
        super().__init__()
        path_label=QLabel('program file:')
        self.pathEdit = QLineEdit()
        path_layout=QHBoxLayout()
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.pathEdit)
        self.pathEdit.setReadOnly(True)
        
        self.dataFile=None
        self.columns=[]
        data_label=QLabel('data file:')
        self.dataEdit=QLineEdit()
        data_layout=QHBoxLayout()
        data_layout.addWidget(data_label)
        data_layout.addWidget(self.dataEdit)
        self.dataEdit.setReadOnly(True)
        
        pathGrid = QVBoxLayout()
        pathGrid.addLayout(path_layout)
        pathGrid.addLayout(data_layout)
        
        self.setLayout(pathGrid)
        
        self.program=None    #参照
        self.module=None    #文字列
        
    def showDialog(self):
        #ファイルが指定される度にimportが実際に実行されるようにし、pathが溜まらないようにする
        path = QFileDialog.getOpenFileName(self, 'select a program')
        self.importFile(path[0])
        
    def rePressed(self):
        self.importFile(self.pathEdit.text())
        
    def tempPressed(self):
        path = QFileDialog.getSaveFileName(self, 'create a template','template.py')
        if not path[0]=='':
            UserClassBase.copyTemplate(path[0])
            self.importFile(path[0])
            
    def copyFile(self,source_path):
        path = QFileDialog.getSaveFileName(self, 'create a copy of the example','example.py')
        if not path[0]=='':
            import shutil
            shutil.copyfile(source_path, path[0])
            
    def showDataDialog(self):
        #ファイルを作れたらTrueを返す
        path = QFileDialog.getSaveFileName(self, 'create a file to write data')
        if not path[0]=='':
            self.dataEdit.setText(path[0])
            self.data_file_init(path[0],self.get_output_labels(),self.get_file_columns_with_unit())
            return True
        else:
            return False
            
    def importFile(self,path):
#        path=repr(path)
        if self.checkFile(path):    #.pyファイル以外（キャンセルも含む)は何もしない
            pre_path=self.pathEdit.text()
            if not pre_path=='':    #''でないということはimportが行われた後ということなのでこれを除去する
                folder=os.path.split(pre_path)[0]
                if sys.path[0]==folder:
                    sys.path.pop(0)
                    sys.modules.pop(self.module)
            
            #programをモジュールとして読み込んでグラフの軸の選択肢をMyQComboBoxに通知    
            self.pathEdit.setText(path)
            folder=os.path.split(path)[0]
            fname=os.path.split(path)[1]
            self.module=fname.split('.')[0]
            sys.path.insert(0,folder)   #先頭に追加することでimport時に一番最初に検索される
            self.program= __import__(self.module)
            checkRaipySyntax(self.program)
            self.importSig.emit(True)
            self.outputLabelChangeSig.emit(self.get_output_labels())
            self.outputUnitChangeSig.emit(self.get_output_units())
            self.sliderChangeSig.emit(self.getSliders())
            self.boolChangeSig.emit(self.getBools())
            self.dialChangeSig.emit(self.getDials())
            self.floatChangeSig.emit(self.getFloats())
            self.graphSettingSig.emit(self.get_graph_settings())
        else:
            print('拡張子が.pyで規格を満たしているファイルを指定してください templateボタンで例を出力できます')
            
    def checkFile(self,path):
        try:
            fname=os.path.split(path)[1]
            extension=fname.rsplit('.')[1]
            if extension=='py':
                return True
            else:
                return False
        except:
            return False
        
    def data_file_close(self):
        self.dataFile.close()
        
    def write_data(self,mydict):
        for column in self.columns:
            self.dataFile.write(str(mydict[column])+'\t')
        self.dataFile.write('\n')
        
    def data_file_init(self,file,columns,columns_u):
        #データファイルの初期化 self.columnsはself.write_dataでデータを書き込む時に使う
        self.dataFile=open(file,'a+')
        self.columns=columns
        for column in columns_u:
            self.dataFile.write(column+'\t')
        self.dataFile.write('\n')
        
    def clean_up(self):
        #remove the remaining path to a program from sys.path and remove program from namespace
        if not sys.path[0]=='':
            path=sys.path.pop(0)
            print('removed \''+path+'\' from sys.path')
            sys.modules.pop(self.module)
            print('removed \''+self.module+'\' from sys.modules')
        
    def get_graph_settings(self):
        #グラフのセッティング
        temp=self.program.Output.get_graph_settings()
        return temp

    def get_output_labels(self):
        #液晶用のラベル　単位付き
        try:
            return self.program.Output.get_output_labels()
        except:
            raise AttributeError('cannot get \'output\'s labels\'.Push template-button in setting-tab of the window and see the template.')

    def get_output_units(self):
        #液晶用のラベル　単位無し
        try:
            return self.program.Output.get_output_units()
        except:
            raise AttributeError('cannot get \'output\'s units\'.Push template-button in setting-tab of the window and see the template.')
            
    def get_file_columns_with_unit(self):
        #ファイルのcolumn名　単位付き
        try:
            strings=[label+'('+unit+')' for label,unit in zip(self.program.Output.get_output_labels(),self.program.Output.get_output_units())]
            return strings
        except:
            raise AttributeError('cannot get \'outputs\'.Push template-button in setting-tab of the window and see the template.')
            
    def getBools(self):
        try:
            return self.program.Control.get_bools()
        except:
            raise AttributeError('cannot get \'Bools\'.Push template-button in setting-tab of the window and see the template.')
            
    def getSliders(self):
        try:
            return self.program.Control.get_sliders()
        except:
            raise AttributeError('cannot get \'Sliders\'.Push template-button in setting-tab of the window and see the template.')
    
    def getDials(self):
        try:
            return self.program.Control.get_dials()
        except:
            raise AttributeError('cannot get \'Dials\'.Push template-button in setting-tab of the window and see the template.')
            
    def getFloats(self):
        try:
            return self.program.Control.get_floats()
        except:
            raise AttributeError('cannot get \'floats\'.Push template-button in setting-tab of the window and see the template.')
            
def checkRaipySyntax(program):
    def typeCheck(mylist,mytype):
        for x in mylist:
            if not type(x)==mytype:
                return False
        return True
    
    def graph_settings_check():
        settings=program.Output.graph_settings
        for setting in settings:
            if type(setting)==list:
                try:
                    x=setting[0]
                    ys=setting[1]
                    colors=setting[2]
                    if not type(x)==str:
                        raise Exception('\'xlabel\' must be a string.')
                    elif not typeCheck(ys,str):
                        raise Exception('\'ylabels\' must be a list of strings.')
                    elif not typeCheck(colors,QColor):
                        raise Exception('\'colors\' must be a list of QColor.')
                    else:
                        pass
                except:
                    raise Exception('\'graph_settings\' must be a list of lists. Each list is like this:[xlabel,[ylabels],[colors]].')
            else:
                raise Exception('\'graph_settings\' must be a list of lists. Each list is like this:[xlabel,[ylabels],[colors]].')
        return True
    
    def outputs_check():
        outputs=program.Output.outputs
        for output in outputs:
            if not typeCheck(output,str):
                raise Exception('\'outputs\' must be a list of lists. Each list is like this:[label,unit].')
        return True
    
    def bools_check():
        bools=program.Control.bools
        for mybool in bools:
            if type(mybool)==list:
                try:
                    label=mybool[0]
                    init=mybool[1]
                    if not type(label)==str:
                        raise Exception('\'label\' must be a string.')
                    elif not type(init)==bool:
                        raise Exception('\'initial parameter must be a bool.')
                    else:
                        pass
                except:
                    raise Exception('\'bools\' must be a list of lists. Each list is like this:[label,initial value].')
            else:
                raise Exception('\'bools\' must be a list of lists. Each list is like this:[label,initial value].')
        return True
                
    def floats_check():
        floats=program.Control.floats
        for myfloat in floats:
            if type(myfloat)==list:
                try:
                    label=myfloat[0]
                    init=myfloat[1]
                    if not type(label)==str:
                        raise Exception('\'label\' must be a string.')
                    elif not (type(init)==float or type(init)==int):
                        raise Exception('\'initial parameter\' must be a float.')
                    else:
                        pass
                except:
                    raise Exception('\'floats\' must be a list of lists. Each list is like this:[label,initial value].')
            else:
                raise Exception('\'floats\' must be a list of lists. Each list is like this:[label,initial value].')
        return True
    
    def sliders_check():
        sliders=program.Control.sliders
        dials=program.Control.dials
        sliders=sliders+dials
        for slider in sliders:
            if type(slider)==list:
                try:
                    label=slider[0]
                    values=slider[1:]
                    if not type(label)==str:
                        raise Exception('\'label\' must be a string.')
                    elif not typeCheck(values,int):
                        raise Exception('\'initial value\',\'minimum\' and \'maximum\' must be a int')
                except:
                    raise Exception('\'sliders\' or \'dials\' must be a list of lists. Each list is like this:[label,initial value,minimum,maximum].')
            else:
                raise Exception('\'sliders\' or \'dials\' must be a list of lists. Each list is like this:[label,initial value,minimum,maximum].')
        return True
    
    graph_settings_check()
    outputs_check()
    bools_check()
    floats_check()
    sliders_check()
    return True
            
if __name__=='__main__':
    app = QApplication(sys.argv)
    f=MyPathBox()
    f.show()
    sys.exit(app.exec_())