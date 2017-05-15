# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Wed Apr 12 22:44:32 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(567, 396)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(10, 120, 531, 191))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.pushButton_Process = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Process.setGeometry(QtCore.QRect(210, 10, 341, 27))
        self.pushButton_Process.setObjectName(_fromUtf8("pushButton_Process"))
        self.pushButton_Check_and_save = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Check_and_save.setGeometry(QtCore.QRect(90, 20, 111, 27))
        self.pushButton_Check_and_save.setObjectName(_fromUtf8("pushButton_Check_and_save"))
        self.pushButton_Show_dep_and_save = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Show_dep_and_save.setGeometry(QtCore.QRect(20, 50, 181, 27))
        self.pushButton_Show_dep_and_save.setObjectName(_fromUtf8("pushButton_Show_dep_and_save"))
        self.pushButton_Check = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Check.setGeometry(QtCore.QRect(20, 20, 71, 27))
        self.pushButton_Check.setObjectName(_fromUtf8("pushButton_Check"))
        self.pushButton_Process_renum = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Process_renum.setGeometry(QtCore.QRect(210, 40, 341, 27))
        self.pushButton_Process_renum.setObjectName(_fromUtf8("pushButton_Process_renum"))
        self.pushButton_Process_renum_schedules = QtGui.QPushButton(self.centralwidget)
        self.pushButton_Process_renum_schedules.setGeometry(QtCore.QRect(210, 70, 341, 27))
        self.pushButton_Process_renum_schedules.setObjectName(_fromUtf8("pushButton_Process_renum_schedules"))
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(420, 320, 118, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 567, 27))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_dxf = QtGui.QAction(MainWindow)
        self.actionLoad_dxf.setObjectName(_fromUtf8("actionLoad_dxf"))
        self.menuFile.addAction(self.actionLoad_dxf)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pushButton_Process.setText(_translate("MainWindow", "Process data and save", None))
        self.pushButton_Check_and_save.setText(_translate("MainWindow", "Check and save", None))
        self.pushButton_Show_dep_and_save.setText(_translate("MainWindow", "Show depndence and save", None))
        self.pushButton_Check.setText(_translate("MainWindow", "Check", None))
        self.pushButton_Process_renum.setText(_translate("MainWindow", "Process data with renumerate and save", None))
        self.pushButton_Process_renum_schedules.setText(_translate("MainWindow", "Process data with renumerate, schedules and save", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionLoad_dxf.setText(_translate("MainWindow", "Load dxf ", None))

