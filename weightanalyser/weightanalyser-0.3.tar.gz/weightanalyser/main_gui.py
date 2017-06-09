# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'weightanalyser/main_gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        MainWindow.resize(981, 667)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.fit_ra_label = QtGui.QLabel(self.centralwidget)
        self.fit_ra_label.setObjectName(_fromUtf8("fit_ra_label"))
        self.gridLayout.addWidget(self.fit_ra_label, 0, 0, 1, 1)
        self.disp_ra_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.disp_ra_lineEdit.setObjectName(_fromUtf8("disp_ra_lineEdit"))
        self.gridLayout.addWidget(self.disp_ra_lineEdit, 1, 1, 1, 1)
        self.fit_ra_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.fit_ra_lineEdit.setObjectName(_fromUtf8("fit_ra_lineEdit"))
        self.gridLayout.addWidget(self.fit_ra_lineEdit, 0, 1, 1, 1)
        self.goal_label = QtGui.QLabel(self.centralwidget)
        self.goal_label.setObjectName(_fromUtf8("goal_label"))
        self.gridLayout.addWidget(self.goal_label, 2, 0, 1, 1)
        self.add_mea_Button = QtGui.QPushButton(self.centralwidget)
        self.add_mea_Button.setObjectName(_fromUtf8("add_mea_Button"))
        self.gridLayout.addWidget(self.add_mea_Button, 6, 1, 1, 1)
        self.disp_ra_label = QtGui.QLabel(self.centralwidget)
        self.disp_ra_label.setObjectName(_fromUtf8("disp_ra_label"))
        self.gridLayout.addWidget(self.disp_ra_label, 1, 0, 1, 1)
        self.grid_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.grid_lineEdit.setObjectName(_fromUtf8("grid_lineEdit"))
        self.gridLayout.addWidget(self.grid_lineEdit, 3, 1, 1, 1)
        self.grid_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.grid_checkBox.setObjectName(_fromUtf8("grid_checkBox"))
        self.gridLayout.addWidget(self.grid_checkBox, 3, 0, 1, 1)
        self.goal_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.goal_lineEdit.setObjectName(_fromUtf8("goal_lineEdit"))
        self.gridLayout.addWidget(self.goal_lineEdit, 2, 1, 1, 1)
        self.plot_Button = QtGui.QPushButton(self.centralwidget)
        self.plot_Button.setObjectName(_fromUtf8("plot_Button"))
        self.gridLayout.addWidget(self.plot_Button, 4, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 2, 1, 1)
        self.plot_muscle_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.plot_muscle_checkBox.setObjectName(_fromUtf8("plot_muscle_checkBox"))
        self.gridLayout_2.addWidget(self.plot_muscle_checkBox, 3, 2, 1, 1)
        self.mat = QEMatplotlibWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mat.sizePolicy().hasHeightForWidth())
        self.mat.setSizePolicy(sizePolicy)
        self.mat.setMinimumSize(QtCore.QSize(700, 500))
        self.mat.setMaximumSize(QtCore.QSize(1200, 800))
        self.mat.setObjectName(_fromUtf8("mat"))
        self.gridLayout_2.addWidget(self.mat, 0, 0, 9, 1)
        spacerItem = QtGui.QSpacerItem(18, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 1, 1, 1)
        self.plot_full_weight_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.plot_full_weight_checkBox.setObjectName(_fromUtf8("plot_full_weight_checkBox"))
        self.gridLayout_2.addWidget(self.plot_full_weight_checkBox, 1, 2, 1, 1)
        self.plot_fat_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.plot_fat_checkBox.setObjectName(_fromUtf8("plot_fat_checkBox"))
        self.gridLayout_2.addWidget(self.plot_fat_checkBox, 2, 2, 1, 1)
        self.adjustment_lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.adjustment_lineEdit.setObjectName(_fromUtf8("adjustment_lineEdit"))
        self.gridLayout_2.addWidget(self.adjustment_lineEdit, 6, 2, 1, 1)
        self.adjustment_label = QtGui.QLabel(self.centralwidget)
        self.adjustment_label.setObjectName(_fromUtf8("adjustment_label"))
        self.gridLayout_2.addWidget(self.adjustment_label, 5, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 8, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 981, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "WeightAnalyser", None))
        self.fit_ra_label.setText(_translate("MainWindow", "fit range", None))
        self.goal_label.setText(_translate("MainWindow", "goal", None))
        self.add_mea_Button.setText(_translate("MainWindow", "add measurement", None))
        self.disp_ra_label.setText(_translate("MainWindow", "disp range", None))
        self.grid_checkBox.setText(_translate("MainWindow", "grid", None))
        self.plot_Button.setText(_translate("MainWindow", "plot!", None))
        self.plot_muscle_checkBox.setText(_translate("MainWindow", "plot muscle", None))
        self.plot_full_weight_checkBox.setText(_translate("MainWindow", "plot full weight", None))
        self.plot_fat_checkBox.setText(_translate("MainWindow", "plot fat", None))
        self.adjustment_label.setText(_translate("MainWindow", "Calorie adjustment", None))

from weightanalyser.visualisation import QEMatplotlibWidget
