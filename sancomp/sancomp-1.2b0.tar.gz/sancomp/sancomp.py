import sys
import numpy as np
import calculations
from PyQt4 import QtCore, QtGui, uic, QtWebKit
import re
 
qtCreatorFile = "sancompt.ui" # Enter file here.
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

face = []
face_moduli = []
face_density = []
face_poisson = []
face_g = []
face_tensile = []
face_compressive = []
face_shear = []
core = []
core_moduli = []
core_density = []



class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		#self.laminate.toggled.connect(self.f_laminate)
		#self.radioButton.toggled.connect(self.calc_def)
		self.calcular_f.clicked.connect(self.verify)
		self.calcular_g.clicked.connect(self.verify2)
		self.cb_beam.activated.connect(self.setImage)
		self.save.clicked.connect(self.file_save)
		self.calcular_c.clicked.connect(self.verify_core)
		self.help.clicked.connect(self.openhelp)
		
			
		#filling qcombobox and lists from file nucleo-elasticidade.dat
		global core
		core=[]
		global core_moduli
		core_moduli=[]
		global core_density
		core_density = []
		file = open('nucleo-elasticidade.dat')
		linha=file.readline()
		while(linha):
			core.append(str(linha.split("	")[0]))
			core_moduli.append(float(linha.split("	")[1]))
			core_density.append(float(linha.split("	")[2]))
			linha=file.readline()
		self.cb_core.addItems(core)
		#filling qcombobox and lists from file face-elasticidade-poisson.dat
		global face
		#face=[]
		global face_moduli
		face_moduli=[]
		global face_poisson
		face_poisson=[]
		global face_density
		face_density = []
		global face_g
		face_g = []
		global face_tensile
		face_tensile = []
		global face_compressive
		face_compressive = []
		global face_shear
		face_shear = []
		
		file2=open('face-elasticidade-poisson.dat')
		linha2=file2.readline()
		
		while(linha2):#filling lists
			face.append(str(linha2.split("	")[0]))
			face_moduli.append(float(linha2.split("	")[1]))
			face_poisson.append(float(linha2.split("	")[2]))
			face_density.append(linha2.split("	")[3])
			face_g.append(linha2.split("	")[4])
			face_tensile.append(linha2.split("	")[5])
			face_compressive.append(linha2.split("	")[6])
			face_shear.append(linha2.split("	")[7])
			linha2 = file2.readline()
		self.cb_laminate.addItems(face)#filling combobox
		
		#face.append(str(self.name))
		#face_moduli.append(float(self.ex))
	
	def openhelp(self):
		self.newWindow = Browser()
		self.newWindow.show()
	
	def file_save(self): #save with qfiledialog
		file_extension = "TXT (*.txt)"
		name, filter = QtGui.QFileDialog.getSaveFileNameAndFilter(self, 'Save File', '', file_extension)
		file3 = open(name,'w')
		text = "INPUTS"+"\n"+"\n"+calculations.resp2+"\n"+"\n"+"OUTPUTS"+"\n"+"\n"+calculations.resp
		file3.write(text)
		file3.close()
	
	def setImage(self): #set pixmap when focus change
		if self.cb_beam.currentText() == "Simple-Simple / Point":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v1.png"))
		elif self.cb_beam.currentText() == "Simple-Simple / Uniform":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v2.png"))
		elif self.cb_beam.currentText() == "Free-Fixed / Point":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v3.png"))
		elif self.cb_beam.currentText() == "Free-Fixed / Uniform":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v4.png"))
		elif self.cb_beam.currentText() == "Fixed-Fixed / Point":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v5.png"))
		elif self.cb_beam.currentText() == "Fixed-Fixed / Uniform":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v6.png"))
		elif self.cb_beam.currentText() == "Choose beam...":
			self.pic_beam.setPixmap(QtGui.QPixmap("image/v0.png"))
			
			
	def verify(self): #verifying input data and calculating lamina or assuming data as laminate data
		#if not self.lamina.isChecked() and not self.laminate.isChecked():
		#	self.textBrowser.setText("Select lamina or laminate")
		#	self.textBrowser.setStyleSheet('color: red')
		#elif self.lamina.isChecked(): #calling functions of calculations module to calculate first tab
		#	self.textBrowser.setStyleSheet('color: black')
		#	calculations.lamina(self)
		#elif self.laminate.isChecked():
		#	self.textBrowser.setStyleSheet('color: black')
		#	calculations.laminate(self)
		try: #reading form data and making the treatment of ValueError
			name = str(self.name.toPlainText())
			ex = self.ex.toPlainText()
			ex=float(ex)
			density_f = float(self.density_f.toPlainText())
			gxy = float(self.gxy.toPlainText())
			#g12 = float(g12)
			vxy = float(self.vxy.toPlainText())
			#calculations.save_laminate_temp(self)
			shear_st = float(self.shear_st.toPlainText())
			tensile_st = float(self.tensile_st.toPlainText())
			compressive_st = float(self.compressive_st.toPlainText())
						
			if name == "":
				self.lami_msg.setStyleSheet('color: red')
				self.lami_msg.setText("Insert a name for the custom laminate")
			else:#adding string line in database and updating lists
				face.append(name)
				face_moduli.append(ex)
				face_poisson.append(vxy)
				face_density.append(density_f)
				face_g.append(gxy)
				face_tensile.append(tensile_st)
				face_compressive.append(compressive_st)
				face_shear.append(shear_st)
				linha_face = ("\n"+name+"\t"+str(ex)+"\t"+str(vxy)+"\t"+str(density_f)+"\t"+str(gxy))+"\t"+str(tensile_st)+"\t"+str(compressive_st)+"\t"+str(shear_st)
				with open("face-elasticidade-poisson.dat","a") as arq_face:
					arq_face.write(linha_face)
				self.cb_laminate.addItems(face)
				self.tabWidget.setCurrentIndex(1)
			
		except ValueError: 
			self.lami_msg.setStyleSheet('color: red')
			self.lami_msg.setText("Fill all fields or check if data entered is correct")	

	def verify_core(self):
		try:
			core_name = str(self.core_name.toPlainText())
			density_c = float(self.density_c.toPlainText())
			core_ex = float(self.core_ex.toPlainText())
			if core_name == "":
				self.core_msg.setStyleSheet('color: red')
				self.core_msg.setText("Insert a name for the custom core")
			else:#adding string line in database and updating lists
				core.append(self.core_name)
				core_moduli.append(core_ex)
				core_density.append(density_c)
				linha_core = ("\n"+core_name+"\t"+str(core_ex)+"\t"+str(density_c))
				with open("nucleo-elasticidade.dat", "a") as arq_core:
					arq_core.write(linha_core)
				self.cb_core.addItem(core_name)
				self.tabWidget.setCurrentIndex(1)
				
		except ValueError:
			self.core_msg.setStyleSheet('color: red')
			self.core_msg.setText("Fill all fields or check if data entered is correct" )
		
	def verify2(self):
		try: #reading form data for second tab and making the treatment of ValueError
			laminate_cb = str(self.cb_laminate.currentText())
			core_cb = str(self.cb_core.currentText())
			beam_cb = str(self.cb_beam.currentText())
			load = float(self.load.toPlainText())
			h = float(self.h.toPlainText())
			H = float(self.H.toPlainText())
			b = float(self.b.toPlainText())
			l = float(self.l.toPlainText())
			self.message.setText(" ")
			if H < h:
				self.message.setStyleSheet('color: red')
				self.message.setText("H cannot be less than h")
			else:
				calculations.beam(self,face,face_moduli,face_poisson,core,core_moduli,face_g,face_density,core_density, face_tensile, face_compressive, face_shear)
			
		except ValueError:
			self.message.setStyleSheet('color: red')
			self.message.setText("Fill all fields or check if data entered is correct" )
		lami = "Choose laminate..."
		cor = "Choose core..."
		beam = "Choose beam..."
		if self.cb_laminate.currentText() == lami:
			self.message.setText("Select a laminate")
		elif self.cb_core.currentText() == cor:
			self.message.setText("Select a core")
		elif self.cb_beam.currentText() == beam:
			self.message.setText("Select a beam type")
		
class Browser(QtGui.QMainWindow):

	def __init__(self):
		"""
			Initialize the browser GUI and connect the events
		"""

		QtGui.QMainWindow.__init__(self)
		self.resize(800,600)
		self.centralwidget = QtGui.QWidget(self)

		self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
		self.mainLayout.setSpacing(0)
		self.mainLayout.setMargin(1)

		self.frame = QtGui.QFrame(self.centralwidget)

		self.gridLayout = QtGui.QVBoxLayout(self.frame)
		self.gridLayout.setMargin(0)
		self.gridLayout.setSpacing(0)

		self.horizontalLayout = QtGui.QHBoxLayout()
		self.tb_url = QtGui.QLineEdit(self.frame)
		self.bt_back = QtGui.QPushButton(self.frame)
		self.bt_ahead = QtGui.QPushButton(self.frame)

		self.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
		self.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))

		self.horizontalLayout.addWidget(self.bt_back)
		self.horizontalLayout.addWidget(self.bt_ahead)
		self.horizontalLayout.addWidget(self.tb_url)
		self.gridLayout.addLayout(self.horizontalLayout)

		self.html = QtWebKit.QWebView()
		self.gridLayout.addWidget(self.html)
		self.mainLayout.addWidget(self.frame)
		self.setCentralWidget(self.centralwidget)

		self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
		self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
		self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)

		self.default_url = "https://gcomp-srv01.nuvem.ufrgs.br/pt-br/"
		self.tb_url.setText(self.default_url)
		self.browse()

	def browse(self):
		"""
			Make a web browse on a specific url and show the page on the
			Webview widget.
		"""

		url = self.tb_url.text() if self.tb_url.text() else self.default_url
		self.html.load(QtCore.QUrl(url))
		self.html.show()		
	
	def tutorial(self):
		self.centralwidget = QtGui.QWidget(self)
		self.frame = QtGui.QFrame(self.centralwidget)

		self.gridLayout = QtGui.QVBoxLayout(self.frame)
		self.gridLayout.setMargin(0)
		self.gridLayout.setSpacing(0)

		self.horizontalLayout = QtGui.QHBoxLayout()
		self.tb_url = QtGui.QLineEdit(self.frame)
		self.bt_back = QtGui.QPushButton(self.frame)
		self.bt_ahead = QtGui.QPushButton(self.frame)

		self.bt_back.setIcon(QtGui.QIcon().fromTheme("go-previous"))
		self.bt_ahead.setIcon(QtGui.QIcon().fromTheme("go-next"))

		self.horizontalLayout.addWidget(self.bt_back)
		self.horizontalLayout.addWidget(self.bt_ahead)
		self.horizontalLayout.addWidget(self.tb_url)
		self.gridLayout.addLayout(self.horizontalLayout)

		self.html = QtWebKit.QWebView()
		self.gridLayout.addWidget(self.html)
		self.mainLayout.addWidget(self.frame)
		self.setCentralWidget(self.centralwidget)

		self.connect(self.tb_url, QtCore.SIGNAL("returnPressed()"), self.browse)
		self.connect(self.bt_back, QtCore.SIGNAL("clicked()"), self.html.back)
		self.connect(self.bt_ahead, QtCore.SIGNAL("clicked()"), self.html.forward)

		self.default_url = "https://sancomp.wordpress.com/"
		self.tb_url.setText(self.default_url)
		self.browse()

	
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	app.setWindowIcon(QtGui.QIcon('image/sancomp.ico'))
	window = MyApp()
	window.show()
	sys.exit(app.exec_())