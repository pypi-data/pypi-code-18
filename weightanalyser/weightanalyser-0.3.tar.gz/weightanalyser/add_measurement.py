# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'weightanalyser/add_measurement.ui'
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

class Ui_AddMeasurementWindow(object):
    def setupUi(self, AddMeasurementWindow):
        AddMeasurementWindow.setObjectName(_fromUtf8("AddMeasurementWindow"))
        AddMeasurementWindow.resize(476, 326)
        self.verticalLayout_2 = QtGui.QVBoxLayout(AddMeasurementWindow)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.calendarWidget = QtGui.QCalendarWidget(AddMeasurementWindow)
        self.calendarWidget.setAccessibleName(_fromUtf8(""))
        self.calendarWidget.setObjectName(_fromUtf8("calendarWidget"))
        self.verticalLayout.addWidget(self.calendarWidget)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.date_label = QtGui.QLabel(AddMeasurementWindow)
        self.date_label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.date_label.setObjectName(_fromUtf8("date_label"))
        self.gridLayout.addWidget(self.date_label, 0, 0, 1, 1)
        self.date_lineEdit = QtGui.QLineEdit(AddMeasurementWindow)
        self.date_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.date_lineEdit.setObjectName(_fromUtf8("date_lineEdit"))
        self.gridLayout.addWidget(self.date_lineEdit, 0, 1, 1, 1)
        self.full_weight_label = QtGui.QLabel(AddMeasurementWindow)
        self.full_weight_label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.full_weight_label.setObjectName(_fromUtf8("full_weight_label"))
        self.gridLayout.addWidget(self.full_weight_label, 0, 2, 1, 1)
        self.full_weight_lineEdit = QtGui.QLineEdit(AddMeasurementWindow)
        self.full_weight_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.full_weight_lineEdit.setObjectName(_fromUtf8("full_weight_lineEdit"))
        self.gridLayout.addWidget(self.full_weight_lineEdit, 0, 3, 1, 1)
        self.today_checkBox = QtGui.QCheckBox(AddMeasurementWindow)
        self.today_checkBox.setMaximumSize(QtCore.QSize(100, 16777215))
        self.today_checkBox.setObjectName(_fromUtf8("today_checkBox"))
        self.gridLayout.addWidget(self.today_checkBox, 1, 0, 1, 1)
        self.fat_perc_label = QtGui.QLabel(AddMeasurementWindow)
        self.fat_perc_label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.fat_perc_label.setObjectName(_fromUtf8("fat_perc_label"))
        self.gridLayout.addWidget(self.fat_perc_label, 1, 2, 1, 1)
        self.fat_perc_lineEdit = QtGui.QLineEdit(AddMeasurementWindow)
        self.fat_perc_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.fat_perc_lineEdit.setObjectName(_fromUtf8("fat_perc_lineEdit"))
        self.gridLayout.addWidget(self.fat_perc_lineEdit, 1, 3, 1, 1)
        self.mus_perc_label = QtGui.QLabel(AddMeasurementWindow)
        self.mus_perc_label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.mus_perc_label.setObjectName(_fromUtf8("mus_perc_label"))
        self.gridLayout.addWidget(self.mus_perc_label, 2, 2, 1, 1)
        self.mus_perc_lineEdit = QtGui.QLineEdit(AddMeasurementWindow)
        self.mus_perc_lineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.mus_perc_lineEdit.setObjectName(_fromUtf8("mus_perc_lineEdit"))
        self.gridLayout.addWidget(self.mus_perc_lineEdit, 2, 3, 1, 1)
        self.add_pushButton = QtGui.QPushButton(AddMeasurementWindow)
        self.add_pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.add_pushButton.setObjectName(_fromUtf8("add_pushButton"))
        self.gridLayout.addWidget(self.add_pushButton, 3, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(AddMeasurementWindow)
        QtCore.QMetaObject.connectSlotsByName(AddMeasurementWindow)
        AddMeasurementWindow.setTabOrder(self.full_weight_lineEdit, self.fat_perc_lineEdit)
        AddMeasurementWindow.setTabOrder(self.fat_perc_lineEdit, self.mus_perc_lineEdit)
        AddMeasurementWindow.setTabOrder(self.mus_perc_lineEdit, self.add_pushButton)
        AddMeasurementWindow.setTabOrder(self.add_pushButton, self.today_checkBox)
        AddMeasurementWindow.setTabOrder(self.today_checkBox, self.calendarWidget)
        AddMeasurementWindow.setTabOrder(self.calendarWidget, self.date_lineEdit)

    def retranslateUi(self, AddMeasurementWindow):
        AddMeasurementWindow.setWindowTitle(_translate("AddMeasurementWindow", "Add measurement Window", None))
        self.date_label.setText(_translate("AddMeasurementWindow", "Date", None))
        self.full_weight_label.setText(_translate("AddMeasurementWindow", "Full weight", None))
        self.today_checkBox.setText(_translate("AddMeasurementWindow", "Today ?", None))
        self.fat_perc_label.setText(_translate("AddMeasurementWindow", "Fat perc.", None))
        self.mus_perc_label.setText(_translate("AddMeasurementWindow", "Mus. perc.", None))
        self.add_pushButton.setText(_translate("AddMeasurementWindow", "add", None))

