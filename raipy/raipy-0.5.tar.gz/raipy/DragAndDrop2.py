# -*- coding: utf-8 -*-
"""
Created on Sun May 28 22:03:58 2017

@author: Yuki
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class DragButton(QPushButton):
    MARGIN=5
    STATE=False #True while dragging　
    POSITION=None
    TOP=0
    TOP_RIGHT=1
    RIGHT=2
    BOTTOM_RIGHT=3
    BOTTOM=4
    BOTTOM_LEFT=5
    LEFT=6
    TOP_LEFT=7
    CENTER=8
    
    def __init__(self,*args):
        super().__init__(*args)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.STATE=True
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == Qt.LeftButton:
            self.POSITION=self.getLocation(event.pos())
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.STATE:
            self.transform(self.POSITION,event)
        else:
            position=self.getLocation(event.pos())
            if position==self.CENTER:
                self.setCursor(Qt.SizeAllCursor)
            elif position in [self.TOP,self.BOTTOM]:
                self.setCursor(Qt.SizeVerCursor)
            elif position in [self.LEFT,self.RIGHT]:
                self.setCursor(Qt.SizeHorCursor)
            elif position in [self.TOP_RIGHT,self.BOTTOM_LEFT]:
                self.setCursor(Qt.SizeBDiagCursor)
            else:
                self.setCursor(Qt.SizeFDiagCursor)
        super(DragButton, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.STATE=False
        if self.__mousePressPos is not None:
            moved = event.globalPos() - self.__mousePressPos 
            if moved.manhattanLength() > 3:
                event.ignore()
                return
        super(DragButton, self).mouseReleaseEvent(event)
        
    def getLocation(self,point):
        x=point.x()
        y=point.y()
        geo=self.geometry()
        w=geo.width()
        h=geo.height()
        if x < self.MARGIN:
            if y < self.MARGIN:
                return self.TOP_LEFT
            elif h-self.MARGIN < y:
                return self.BOTTOM_LEFT
            else:
                return self.LEFT
        elif w-self.MARGIN < x:
            if y < self.MARGIN:
                return self.TOP_RIGHT
            elif h-self.MARGIN < y:
                return self.BOTTOM_RIGHT
            else:
                return self.RIGHT
        else:
            if y < self.MARGIN:
                return self.TOP
            elif h-self.MARGIN < y:
                return self.BOTTOM
            else:
                return self.CENTER
                
    def transform(self,position,event):
        globalPos = event.globalPos()
        diff = globalPos - self.__mouseMovePos
        xdiff=diff.x()
        ydiff=diff.y()
        x=self.geometry().x()
        y=self.geometry().y()
        w=self.geometry().width()
        h=self.geometry().height()        
        if position==self.TOP:
            self.setGeometry(x,y+ydiff,w,h-ydiff)
        elif position==self.TOP_RIGHT:
            self.setGeometry(x,y+ydiff,w+xdiff,h-ydiff)
        elif position==self.RIGHT:
            self.setGeometry(x,y,w+xdiff,h)
        elif position==self.BOTTOM_RIGHT:
            self.setGeometry(x,y,w+xdiff,h+ydiff)
        elif position==self.BOTTOM:
            self.setGeometry(x,y,w,h+ydiff)
        elif position==self.BOTTOM_LEFT:
            self.setGeometry(x+xdiff,y,w-xdiff,h+ydiff)
        elif position==self.LEFT:
            self.setGeometry(x+xdiff,y,w-xdiff,h)
        elif position==self.TOP_LEFT:
            self.setGeometry(x+xdiff,y+ydiff,w-xdiff,h-ydiff)
        else:
            currPos = self.mapToGlobal(self.pos())
            newPos = self.mapFromGlobal(currPos + diff)
            self.move(newPos)
        self.__mouseMovePos = globalPos
        
if __name__ == "__main__":
    app = QApplication([])
    w = QWidget()
    w.resize(800,600)

    for i in range(1):
        button = DragButton("Drag", w)

    w.show()
    app.exec_()