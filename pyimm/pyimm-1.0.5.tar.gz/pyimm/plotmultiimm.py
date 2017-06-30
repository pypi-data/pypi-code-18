'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''
import sys
import traceback
import signal
import PyQt4.QtGui as qtGui
import PyQt4.QtCore as qtCore
#import PyQt4.QtCore.Qt as qt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt 
from matplotlib.colors import LogNorm, NoNorm

import  pyimm.immheader as header
import pyimm.GetImmStartIndex as gsi
import  pyimm.OpenMultiImm as multiImm
import random

class PlotMultiImm(qtGui.QMainWindow):
    
    def __init__(self, parent=None):
        super(PlotMultiImm, self).__init__(parent)
        self.plotRange = (0,255)
        layout = qtGui.QVBoxLayout()
        mainWindow = qtGui.QWidget()
        self.fileEntry = FileEntry()
        self.plotWindow = PlotWindow()
        self.imageSelection = ImageSelection()
        
        layout.addWidget(self.fileEntry)
        layout.addWidget(self.plotWindow)
        layout.addWidget(self.imageSelection)
        
        mainWindow.setLayout(layout)
        self.setCentralWidget(mainWindow)
        self.connect(self.fileEntry, qtCore.SIGNAL("immFileChanged"),
                     self._immFileChanged)
        self.connect(self.plotWindow, qtCore.SIGNAL("immDataChanged"),
                     self._immDataChanged)
        self.connect(self.imageSelection, qtCore.SIGNAL("imageNumChanged(int)"),
                     self._imgNumChanged)
        self.connect(self.imageSelection, 
                     qtCore.SIGNAL("updateImage()"),
                     self.updateImage)
        self.connect(self.plotWindow, 
                     qtCore.SIGNAL("updateImage()"),
                     self.updateImage)
        
    def _displaySelectedImage(self):
        print ("PlotMultiImm.displaySelectedImage")
        self.plotWindow.updateImage(self.imageSelection.getSelectedValue())
        
    def _displaySummedImage(self):
        print ("PlotMultiImm.displaySelectedImage")
        self.plotWindow.updateSummedImage(self.imageSelection.getSummedRange())
        
    def _immFileChanged(self):
        print("IMM FileChanged")
        self.plotWindow.setIMMFile(self.fileEntry.getFileName())
     
    def _immDataChanged(self):
        numImages = self.plotWindow.getNumberOfImages()
        self.imageSelection.setRange(1, numImages) 
        
    def _imgNumChanged(self, imgNum):
        print ("updating" + str(imgNum))
        self.plotWindow.updateImage(imgNum) 
        
    def updateImage(self):
        print ("PlotMultiImm.updateChanged")
        if self.imageSelection.getSelectionType() == \
                    ImageSelection.SELECTED_IMAGE:
            selectedImage = self.imageSelection.getSelectedValue()
            self.plotWindow.setPlotRange(self.imageSelection.getPlotRange())
            
            self.plotWindow.updateImage(selectedImage)
        elif self.imageSelection.getSelectionType() == \
                    ImageSelection.SUMMED_IMAGE:
            imageRange = self.imageSelection.getSummedRange()
            self.plotWindow.setPlotRange(self.imageSelection.getPlotRange())
            self.plotWindow.updateSummedImage(imageRange)
            
class FileEntry(qtGui.QDialog):
    def __init__(self, parent=None):
        super(FileEntry, self).__init__(parent)
        self.filename = None
        layout = qtGui.QHBoxLayout()
        
        label = qtGui.QLabel("IMM File: ")
        self.fileNameText = qtGui.QLineEdit()
        self.browseBtn = qtGui.QPushButton("Browse")
        
        layout.addWidget(label)
        layout.addWidget(self.fileNameText)
        layout.addWidget(self.browseBtn)
        
        self.connect(self.browseBtn, \
                     qtCore.SIGNAL("clicked()"), \
                self._browseImmFile)
        self.connect(self.fileNameText, \
                     qtCore.SIGNAL("editingFinished()"), \
                     self._immFileChanged)
        self.setLayout(layout)
        
    def _browseImmFile(self):
        print ("Browse Btn")
        fileName = qtGui.QFileDialog.getOpenFileName(None, \
                                               "Select IMM file", \
                                               filter="*.imm")
        self.fileNameText.setText(str(fileName))
        
        self.emit(qtCore.SIGNAL("immBrowsingChanged"))

    def _immFileChanged(self):
        filename = self.getFileName()
        if filename != self.filename:
            filename = self.filename
            self.emit(qtCore.SIGNAL("immFileChanged"))
        
    def getFileName(self):
        return str(self.fileNameText.text())
        

class PlotWindow(qtGui.QDialog):
    def __init__(self, parent=None):
        super(PlotWindow, self).__init__(parent)
        self.plotRange = (0,255)
        layout = qtGui.QVBoxLayout()
        self.startIndex = None
        self.dlen = None
        self.filename = None
        self.firstPass = True
        self.figure = plt.figure()
        self.logPlotNorm = None
        
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        self.logSelectContainer = qtGui.QWidget()
        logSelectLayout = qtGui.QHBoxLayout()
        self.logPlotSelect = qtGui.QCheckBox("Log Plot")
        
        logSelectLayout.addWidget(self.logPlotSelect)
        self.logSelectContainer.setLayout(logSelectLayout)
        
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.logSelectContainer)

        self.connect(self.logPlotSelect, 
                     qtCore.SIGNAL("stateChanged(int)"),
                     self._logSelectChanged)
        self.setLayout(layout)
        
    def setIMMFile(self, filename):
        try:
            self.filename = filename
            fp = open(filename, "r")
            numberOfImages = header.getNumberOfImages(fp)
            
            self.startIndex, self.dlen = \
                gsi.GetStartPositions(filename, numberOfImages)
    
            self.updateImage(1)
            fp.close()
            self.emit(qtCore.SIGNAL("immDataChanged"))
        except Exception as ex:
            print "Error with file " + str(ex)

    def getNumberOfImages(self):
        return len(self.startIndex)
    
    def _logSelectChanged(self, int):
        if self.logPlotSelect.isChecked():
            self.logPlotNorm = LogNorm()
        else:
            self.logPlotNorm = NoNorm()
        self.emit(qtCore.SIGNAL("updateImage()"))
    
    def setPlotRange(self, plotRange):
        print "setting plotRange"
        self.plotRange = plotRange
        
    def updateImage(self, imageNum):
        print("in updateImage: " + str(imageNum) )
        try:
            print("in updateImage: start Trying " + str(imageNum) )
            data = multiImm.OpenMultiImm(self.filename, 
                                         imageNum-1, 1, 
                                         self.startIndex,self.dlen)[0]
            fp = open(self.filename, "r")
            hdr = header.readHeader(fp, self.startIndex[imageNum-1])
            fp.close()
            data.reshape((hdr['cols'],hdr['rows']))
            if self.firstPass == True:
                print("first Pass")
                ax = self.figure.add_subplot(111)
                
                #ax.hold(False)
                self.img = ax.imshow(data, norm=self.logPlotNorm)
                self.img.set_clim(self.plotRange[0],self.plotRange[1])
                self.img.set_cmap(plt.cm.gray)
                self.firstPass = False
            else:
                self.img.set_data(data)
                self.img.set_norm(self.logPlotNorm)
                self.img.set_clim(self.plotRange[0],self.plotRange[1])
                self.img.set_cmap(plt.cm.gray)
            self.canvas.draw()
            print("in updateImage: done Trying " + str(imageNum) )
        except Exception as ex:
            print "updateImage Error " + str(ex)
            #raise ex 
    
    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # discards the old graph
        ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
        
    def updateSummedImage(self, range):
        print ("Updating summed Range to " + str(range[0]) + \
               " - " + str(range[1]))
        try:
            print("in updateSum: start Trying " + str(range[0]) + \
               " - " + str(range[1]))
            data = multiImm.SumMultiImm(self.filename, 
                                         range[0], range[1]-range[0], 
                                         self.startIndex,self.dlen)
            fp = open(self.filename, "r")
            hdr = header.readHeader(fp, self.startIndex[range[0]])
            fp.close()
            data.reshape((hdr['cols'],hdr['rows']))
            if self.firstPass == True:
                print("first Pass")
                ax = self.figure.add_subplot(111)
                
                self.img = ax.imshow(data, norm=self.logPlotNorm)
                self.img = ax.imshow(data)
                self.firstPass = False
            else:
                self.img.set_data(data)
                self.img.set_norm(self.logPlotNorm)
            self.canvas.draw()
        except Exception as ex:
            print "updateImage Error " + str(ex)
            traceback.print_exc(file = sys.stdout)
        
        
class ImageSelection(qtGui.QDialog):
    SUMMED_IMAGE = "summedImage"
    SELECTED_IMAGE = "selectedImage"
    
    def __init__(self, parent=None):
        super(ImageSelection, self).__init__(parent)
        self.sumMinValue = 0
        self.sumMaxValue = 1
        self.plotMinValue = 0
        self.plotMaxValue = 255
        
        layout = qtGui.QVBoxLayout()
        
        self.sliderContainer = qtGui.QWidget()
        sliderLayout = qtGui.QVBoxLayout()
        self.label = qtGui.QLabel()
        self.slider = qtGui.QSlider()
        self.slider.setOrientation(qtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(qtCore.Qt.StrongFocus)
        self.label.setText(str(self.slider.value()))
        sliderLayout.addWidget(self.label)
        sliderLayout.addWidget(self.slider)
        self.sliderContainer.setLayout(sliderLayout)

        self.plotMinContainer = qtGui.QWidget()
        plotMinLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("Plot Min")
        self.plotMin = qtGui.QLineEdit(str(self.plotMinValue))
        self.plotMinValidator = qtGui.QIntValidator(0, 65000)
        self.plotMin.setValidator(self.plotMinValidator)
        plotMinLayout.addWidget(label)
        plotMinLayout.addWidget(self.plotMin)
        self.plotMinContainer.setLayout(plotMinLayout)

        self.plotMaxContainer = qtGui.QWidget()
        plotMaxLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("plot Max")
        self.plotMax = qtGui.QLineEdit(str(self.plotMaxValue))
        self.plotMaxValidator = qtGui.QIntValidator(0, 65000)
        self.plotMax.setValidator(self.plotMaxValidator)
        plotMaxLayout.addWidget(label)
        plotMaxLayout.addWidget(self.plotMax)
        self.plotMaxContainer.setLayout(plotMaxLayout)
        layout.addWidget(self.plotMinContainer)
        layout.addWidget(self.plotMaxContainer)
       
        sumLayout = qtGui.QVBoxLayout()
        self.showSums = qtGui.QCheckBox("Display Sums")
        # setup Minimum Input
        self.sumMinContainer = qtGui.QWidget()
        sumMinLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("Sum Min")
        self.sumMin = qtGui.QLineEdit(str(self.sumMinValue))
        self.sumMinValidator = qtGui.QIntValidator(0, 100)
        self.sumMin.setValidator(self.sumMinValidator)
        sumMinLayout.addWidget(label)
        sumMinLayout.addWidget(self.sumMin)
        self.sumMinContainer.setLayout(sumMinLayout)
        self.sumMinContainer.setEnabled(False)
        # setup Maximum Input
        self.sumMaxContainer = qtGui.QWidget()
        sumMaxLayout = qtGui.QHBoxLayout()
        label = qtGui.QLabel("Sum Max")
        self.sumMax = qtGui.QLineEdit(str(self.sumMaxValue))
        self.sumMaxValidator = qtGui.QIntValidator(0, 100)
        self.sumMax.setValidator(self.sumMaxValidator)
        sumMaxLayout.addWidget(label)
        sumMaxLayout.addWidget(self.sumMax)
        self.sumMaxContainer.setLayout(sumMaxLayout)
        self.sumMaxContainer.setEnabled(False)
        #combine sumLayout
        
        sumLayout.addWidget(self.showSums)
        
        sumLayout.addWidget(self.sumMinContainer)
        sumLayout.addWidget(self.sumMaxContainer)
        #
        layout.addWidget(self.sliderContainer)
        layout.addLayout(sumLayout)
        
        self.setLayout(layout)
        self.connect (self.slider, \
                      qtCore.SIGNAL("valueChanged(int)"),
                      self._selectionChanged)
        self.connect (self.slider, \
                      qtCore.SIGNAL("sliderMoved(int)"),
                      self._updateLabel)
        self.connect (self.slider, \
                      qtCore.SIGNAL("valueChanged(int)"),
                      self._updateLabel)
        self.connect(self.plotMin, \
                     qtCore.SIGNAL("editingFinished()"), \
                     self._plotRangeChanged)
        self.connect(self.plotMax, \
                     qtCore.SIGNAL("editingFinished()"), \
                     self._plotRangeChanged)
        self.connect(self.showSums, \
                      qtCore.SIGNAL("stateChanged(int)"), \
                      self._showSumsChanged)
        self.connect(self.sumMin, \
                     qtCore.SIGNAL("editingFinished()"), \
                     self._sumRangeChanged)
        self.connect(self.sumMax, \
                     qtCore.SIGNAL("editingFinished()"), \
                     self._sumRangeChanged)
        
    def getPlotRange(self):
        return (self.plotMinValue, self.plotMaxValue)
    def getSelectedValue(self):
        return int(self.slider.value())
    
    def getSummedRange(self):
        return (int(self.sumMin.text()), int(self.sumMax.text()))
    
    def getSelectionType(self):
        if self.showSums.isChecked():
            return ImageSelection.SUMMED_IMAGE
        else:
            return ImageSelection.SELECTED_IMAGE
            
    def _selectionChanged(self, value):
        print ("in selection changed")
        self.emit(qtCore.SIGNAL("imageNumChanged(int)"), value)
        
    def setRange(self, minVal, maxVal):
        self.slider.setRange(minVal,maxVal)
        self.sumMinValidator.setRange(minVal, maxVal)
        self.sumMaxValidator.setRange(minVal, maxVal)
        self.sumMin.setText(str(minVal))
        self.sumMax.setText(str(maxVal))
        self.sumMaxValue = maxVal
        self.sumMinValue = minVal
        
    def _showSumsChanged(self, intValue):
        if self.showSums.isChecked():
            self.sliderContainer.setEnabled(False)
            self.sumMinContainer.setEnabled(True)
            self.sumMaxContainer.setEnabled(True)
        else:
            self.sliderContainer.setEnabled(True)
            self.sumMinContainer.setEnabled(False)
            self.sumMaxContainer.setEnabled(False)
        self.emit(qtCore.SIGNAL("updateImage()"))
            
    def _plotRangeChanged(self):
        minVal = int(self.plotMin.text())
        maxVal = int(self.plotMax.text())
        if minVal != self.plotMinValue or maxVal != self.plotMaxValue:
            if maxVal >= minVal:
                print ("_sumRangeChanged Flagging with displaySummedImage()")
                self.plotMinValue = minVal
                self.plotMaxValue = maxVal
                self.emit(qtCore.SIGNAL("updateImage()"))
 
    def _sumRangeChanged(self):
        minVal = int(self.sumMin.text())
        maxVal = int(self.sumMax.text())
        if minVal != self.sumMinValue or maxVal != self.sumMaxValue:
            if maxVal >= minVal:
                print ("_sumRangeChanged Flagging with displaySummedImage()")
                self.sumMinValue = minVal
                self.sumMaxValue = maxVal
                self.emit(qtCore.SIGNAL("updateImage()"))
        
    def _updateLabel(self, value):
        self.label.setText(str(value))

def ctrlCHandler(signal, frame):
    qtGui.QApplication.closeAllWindows()
    
#This line allows CTRL_C to work with PyQt.
signal.signal(signal.SIGINT, ctrlCHandler)
app = qtGui.QApplication(sys.argv)
mainForm = PlotMultiImm()
mainForm.show()
#timer allows Python interupts to work
timer = qtCore.QTimer()
timer.start(1000)
timer.timeout.connect(lambda: None)
app.exec_()