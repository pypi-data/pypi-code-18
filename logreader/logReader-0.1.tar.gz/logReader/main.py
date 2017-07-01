#!/bin/python3
import re
import sys
from time import time
import os

import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5.uic import loadUi
from dateutil import parser

__author__ = 'MyrikLD'
__email__ = 'myrik260138@tut.by'
__license__ = 'GPLv3'

PATH = os.path.dirname(__file__)

with open(PATH+'/default.yaml') as data:
	config = yaml.load(data)

pattern = config['pattern']
colors = config['colors']
lvls = config['levels']


def pattList(patt):
	p = '(\(\?P<(?P<data>[\w]+)>[^)]+\))'
	ret = re.findall(p, patt)
	return [i[1] for i in ret]


class Level(object):
	def __init__(self, data):
		self.text = str(data)
		try:
			self.num = lvls.index(self.text)
		except Exception:
			self.num = 0

	def __str__(self):
		return str(self.text)

	def __eq__(self, other):
		t = type(other)
		if t == Level:
			return self.num == other.num
		elif t == str:
			return self.text == other
		elif t == int:
			return self.num == other
		else:
			return False


class LineList(list):
	def filter(self, lf):
		return LineList(filter(lambda x: x.get('level') in lf, self))

	def get(self, num, pole, tf=3):
		i = self[num]
		if type(pole) == list:
			m = list()
			for p in pole:
				if p.lower() == 'time':
					if tf == 0:
						m.append(str(i[p]))
					elif tf == 1:
						m.append(str(i[p].date()))
					elif tf == 2:
						m.append(str(i[p].time()))
					elif tf == 3:
						if num > 0:
							m.append(str((i[p] - self[num - 1][p])))
						else:
							m.append(str(i[p]))
				elif p.lower() == 'level':
					m.append(str(i[p]))
				else:
					m.append(i[p])
			return m
		else:
			if pole == 'time':
				if tf == 0:
					return str(i[pole])
				elif tf == 1:
					return str(i[pole].date())
				elif tf == 2:
					return str(i[pole].time())
				elif tf == 3:
					if num > 0:
						sub = i[pole] - self[num - 1][pole]
						return str(sub)
					else:
						return str(i[pole])
			else:
				return str(i[pole])

	def parse(self, data, patt):
		ret = re.match(patt, data, re.IGNORECASE)
		if ret is None:
			print('Regexp error')
			return
		ret = ret.groupdict()
		for key in ret.keys():
			if key == 'time':
				ret[key] = parser.parse(ret[key])
			elif key == 'level':
				ret[key] = Level(ret[key])
		self.append(dict(ret))


class DemoImpl(QMainWindow):
	lineList = None
	filename = None

	def __init__(self, *args):
		super(DemoImpl, self).__init__(*args)

		loadUi(PATH+'/ui.ui', self)
		self.reApplyBtn.clicked.connect(self.reApply)
		self.parApplyBtn.clicked.connect(self.parApply)
		self.actionOpen.triggered.connect(self.openFile)
		self.actionHelp.triggered.connect(self.help)
		self.actionExit.triggered.connect(lambda: exit(0))

		self.reLine.setText(pattern)

		self.box = dict()
		self.box.update({lvls[0]: self.boxDEBUG})
		self.box.update({lvls[1]: self.boxINFO})
		self.box.update({lvls[2]: self.boxWARNING})
		self.box.update({lvls[3]: self.boxERROR})
		self.box.update({lvls[4]: self.boxCRITICAL})
		for i in self.box.values():
			i.clicked.connect(self.update)
		self.dfBox.currentIndexChanged.connect(self.update)

		self.paramsList.setText(', '.join(pattList(pattern)))
		self.update()

	def keyPressEvent(self, QKeyEvent):
		mod, scan = QKeyEvent.nativeModifiers(), QKeyEvent.nativeScanCode()
		if mod == 20 and scan == 54:
			a = self.tableView.selectedIndexes()
			if len(a) == 0:
				return None

			dd = {}
			for i in a:
				row = i.row()
				data = i.data()
				if row in dd:
					dd[row].append(data)
				else:
					dd.update({row: [data]})

			text = str()
			for i in sorted(dd.keys()):
				text += '\t'.join(dd[i]) + '\n'

			cb = QApplication.clipboard()
			cb.clear(mode=cb.Clipboard)
			cb.setText(text[:-1], mode=cb.Clipboard)

	def readFile(self, fn):
		if fn is None or len(fn) == 0:
			return None
		self.filename = fn
		f = open(self.filename)

		lc = 0
		lp = 0
		self.lineList = LineList()
		self.Loading.setFormat('%p%')
		self.Loading.setValue(0)
		f = list(f)
		st = time()
		for i in f:
			self.lineList.parse(i, pattern)
			lc += 1
			proc = (lc * 100) / len(f)
			if proc != lp:
				lp = proc
				self.Loading.setValue(lp)
		st = time() - st
		self.Loading.setFormat('Parsed %i lines in %f sec' % (len(list(f)), st))
		self.update()

	def lvlFilter(self):
		return [Level(i) for i in filter(lambda x: self.box[x].isChecked(), self.box.keys())]

	def update(self):
		if self.lineList is None:
			return

		self.tm = MyTableModel(self.lineList.filter(self.lvlFilter()), self.header, self)
		self.tableView.setModel(self.tm)

	def reApply(self):
		pattern = str(self.reLine.text())
		patstr = ', '.join(pattList(pattern))
		self.paramsList.setText(patstr)

		self.pattParse()
		self.readFile(self.filename)

	def pattParse(self):
		global pattern
		pattern = str(self.reLine.text())
		self.header = self.paramsList.text().replace(' ', '').split(',')

	def parApply(self):
		self.pattParse()
		self.update()

	def openFile(self):
		dia = QFileDialog()
		fname = dia.getOpenFileName(caption='Open file', directory='/home')[0]
		dia.close()
		if len(fname) > 0:
			self.pattParse()
			self.readFile(fname)

	def help(self):
		self.helpWindow = Help()


class MyTableModel(QAbstractTableModel):
	def __init__(self, datain, headerdata, parent=None):
		QAbstractTableModel.__init__(self, parent)
		self.arraydata = datain
		self.headerdata = headerdata

	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.headerdata)

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			if role == Qt.ToolTipRole:
				column = self.headerdata[index.column()]
				df = widget.dfBox.currentIndex()
				itm = self.arraydata.get(index.row(), column, df)
				return QVariant(itm)
			if role == Qt.BackgroundColorRole:
				lvl = self.arraydata[index.row()].get('level', 0)
				return QVariant(QColor(colors[lvl.num]))
			return QVariant()
		itm = self.arraydata.get(index.row(), self.headerdata[index.column()], widget.dfBox.currentIndex())
		return QVariant(itm)

	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.headerdata[section])
		return QVariant()


class Help(QDialog):
	def __init__(self):
		super().__init__()
		loadUi(PATH+'/about.ui', self)
		self.show()

widget = None

def main():
	global widget
	app = QApplication(sys.argv)
	widget = DemoImpl()
	widget.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
