#!/bin/python3
import argparse
import os
import re
import sys
from datetime import datetime
from time import time

import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog
from PyQt5.uic import loadUi
from dateutil import parser

__author__ = 'MyrikLD'
__email__ = 'myrik260138@tut.by'
__license__ = 'GPLv3'
__version__ = '0.7.6'

PATH = os.path.dirname(__file__)
HOME = os.path.expanduser("~")
CONFIGPATH = None


def pattList(patt):
	p = '(\(\?P<(?P<data>[\w]+)>[^)]+\))'
	ret = re.findall(p, patt)
	return [i[1] for i in ret]


class dt(datetime):
	def show(self, var=0):
		if isinstance(var, int):
			if var == 0:
				return str(self)
			elif var == 1:
				return str(self.date())
			elif var == 2:
				return str(self.time())
			else:
				return str(self)
		return str(self - var)

	@classmethod
	def new(cls):
		return cls.now().replace(hour=0, minute=0, second=0, microsecond=0)


class Level(object):
	config = None

	def __init__(self, data=None):
		self.text = str(data)
		try:
			self.num = self.config['levels'].index(self.text)
		except Exception:
			self.num = 1
		try:
			self.color = self.config['colors'][self.num]
		except Exception:
			self.color = 'white'

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
		return LineList(filter(lambda x: x.level in lf, self))


class Line(object):
	struct = {}
	level = Level()
	time = dt.new()
	result = False

	def __init__(self, data, patt=None):
		self.text = data
		if patt is not None:
			self.parse(patt)

	def parse(self, patt):
		ret = re.match(patt, self.text, re.IGNORECASE)
		if ret is None:
			self.result = False
			print('Regexp error: ' + self.text)
			return self
		ret = dict(ret.groupdict())
		for key in list(ret.keys()):
			if key == 'time':
				self.time = parser.parse(ret[key], default=dt.new())
				del ret[key]
			elif key == 'level':
				self.level = Level(ret[key])
				del ret[key]
		self.struct = dict(ret)
		self.result = True
		return self

	def show(self, pole, tf=3):
		if isinstance(pole, list):
			m = list()
			for p in pole:
				if p == 'time':
					m.append(self.time.show(tf))
				elif p == 'level':
					m.append(str(self.level))
				else:
					m.append(str(self.struct[p]))
			return m
		else:
			if pole == 'time':
				return self.time.show(tf)
			elif pole == 'level':
				return str(self.level)
			else:
				return str(self.struct[pole])

	def __str__(self):
		return str(self.text)


class DemoImpl(QMainWindow):
	lineList = LineList()
	filename = None

	def __init__(self, config=None, file=None, *args):
		super(DemoImpl, self).__init__(*args)
		Level.config = config

		loadUi(PATH + '/ui.ui', self)
		self.reApplyBtn.clicked.connect(self.reApply)
		self.parApplyBtn.clicked.connect(self.parApply)
		self.actionOpen.triggered.connect(self.openFile)
		self.actionHelp.triggered.connect(self.help)
		self.actionExit.triggered.connect(lambda: exit(0))
		self.dfBox.currentIndexChanged.connect(self.upd)

		self.box = dict()
		self.box.update({config['levels'][0]: self.boxDEBUG})
		self.box.update({config['levels'][1]: self.boxINFO})
		self.box.update({config['levels'][2]: self.boxWARNING})
		self.box.update({config['levels'][3]: self.boxERROR})
		self.box.update({config['levels'][4]: self.boxCRITICAL})
		for i in self.box.values():
			i.clicked.connect(self.upd)

		self.pattern = config['pattern']
		self.reLine.setText(self.pattern)
		self.paramsList.setText(', '.join(pattList(self.pattern)))

		self.upd()

		if file is not None:
			self.readFile(file)

	def keyPressEvent(self, QKeyEvent):
		mod, key = QKeyEvent.modifiers(), QKeyEvent.key()
		if mod == Qt.ControlModifier and key == Qt.Key_C:
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
		elif mod == Qt.ControlModifier and key == Qt.Key_V:
			clipboard = QApplication.clipboard()
			mimeData = clipboard.mimeData()
			data = mimeData.text().split('\n')
			while '' in data:
				data.remove('')
			if len(data) > 0:
				self.parseStrings(data)

	def readFile(self, fn):
		if fn is None or len(fn) == 0:
			return None
		self.filename = fn
		try:
			f = list(open(self.filename))
			self.parseStrings(f)
		except Exception as e:
			print(e)

	def parseStrings(self, data):
		if len(data) == 0:
			return
		if not Line(data[0], self.pattern).result:
			print('Input data error')
			return
		self.Loading.setFormat('%p%')
		self.Loading.setValue(0)
		print('Parsing %i lines...' % (len(data)))
		st = time()
		data = [Line(i) for i in data]
		self.Loading.setValue(1)
		for i in range(len(data)):
			data[i].parse(self.pattern)
			proc = int(i * 100 / len(data))
			if proc > self.Loading.value():
				self.Loading.setValue(proc)
		self.Loading.setValue(100)
		st = time() - st
		print('Parsed %i lines in %f sec' % (len(data), st))
		self.Loading.setFormat('Parsed %i lines in %f sec' % (len(data), st))
		if len(data) > 0:
			self.lineList = LineList(data)
			self.upd()
		self.tableView.scrollToBottom()

	def lvlFilter(self):
		return [Level(i) for i in filter(lambda x: self.box[x].isChecked(), self.box.keys())]

	def upd(self):
		if self.lineList is None:
			return
		self.header = self.paramsList.text().replace(' ', '').split(',')
		self.tm = MyTableModel(self.lineList.filter(self.lvlFilter()), self.header, self)
		self.tableView.setModel(self.tm)

	def reApply(self):
		self.pattern = str(self.reLine.text())
		self.paramsList.setText(', '.join(pattList(self.pattern)))

		if len(self.lineList) == 0:
			return

		print('Updating %i lines...' % len(self.lineList))
		self.Loading.setFormat('%p%')
		self.Loading.setValue(0)
		st = time()

		for i in range(len(self.lineList)):
			proc = int(i * 100 / len(self.lineList))
			if proc > self.Loading.value():
				self.Loading.setValue(proc)
			self.lineList[i].parse(self.pattern)

		self.Loading.setValue(100)
		st = time() - st
		print('Updated %i lines in %f sec' % (len(self.lineList), st))
		self.Loading.setFormat('Updated %i lines in %f sec' % (len(self.lineList), st))

		self.upd()

	def parApply(self):
		a = self.paramsList.text().replace(' ', '').split(',')
		b = pattList(self.pattern)
		for i in a:
			if i not in b:
				print('Unknown param: ' + str(i))
				return
		self.upd()

	def openFile(self):
		dia = QFileDialog()
		fname = dia.getOpenFileName(caption='Open file', directory=HOME)[0]
		dia.close()
		if len(fname) > 0:
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

	def data(self, index, role=None):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			if role == Qt.ToolTipRole:
				return self.data(index)
			if role == Qt.BackgroundColorRole:
				lvl = self.arraydata[index.row()].level
				return QVariant(QColor(lvl.color))
			return QVariant()

		tm = widget.dfBox.currentIndex()
		if tm == 3 and index.row() > 0:
			tm = self.arraydata[index.row() - 1].time

		itm = self.arraydata[index.row()].show(self.headerdata[index.column()], tm)
		return QVariant(itm)

	def headerData(self, section, orientation, role):
		if orientation == Qt.Horizontal and role == Qt.DisplayRole:
			return QVariant(self.headerdata[section])
		return QVariant()


class Help(QDialog):
	def __init__(self):
		super().__init__()
		loadUi(PATH + '/about.ui', self)
		self.show()


widget = None


def main():
	global widget
	args = argparse.ArgumentParser(description='PyQt5 programm for parse and reading any log file.')
	args.add_argument('-v', '--version', action='version', version='LogReader ' + str(__version__))
	args.add_argument('-c', dest='config', help='config path')
	args.add_argument('-f', dest='file', help='file path')
	args = args.parse_args()

	if args.config is not None and not os.path.isfile(str(args.config)):
		print('Unavailable path: ' + str(args.config))
	if os.path.isfile(str(args.config)):
		CONFIGPATH = args.config

		with open(CONFIGPATH) as data:
			print('Config file: ' + CONFIGPATH)
			config = yaml.load(data)
	elif os.path.isfile(HOME + '/.logreader'):
		CONFIGPATH = HOME + '/.logreader'

		with open(CONFIGPATH) as data:
			print('Config file: ' + CONFIGPATH)
			config = yaml.load(data)
	else:
		CONFIGPATH = PATH + '/default.yaml'

		with open(CONFIGPATH) as data:
			print('Default config file: ' + CONFIGPATH)
			config = yaml.load(data)

		if not os.path.isfile(HOME + '/.logreader'):
			print('Create config file: ' + HOME + '/.logreader')
			try:
				with open(HOME + '/.logreader', 'w+') as outfile:
					yaml.dump(config, outfile)
			except Exception:
				pass
	file = None
	if args.file is not None and not os.path.isfile(str(args.file)):
		print('Unavailable path: ' + str(args.file))
		file = None
	elif os.path.isfile(str(args.file)):
		print('Input file: ' + str(args.file))

	app = QApplication(sys.argv)
	widget = DemoImpl(config=config, file=file)
	widget.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()
