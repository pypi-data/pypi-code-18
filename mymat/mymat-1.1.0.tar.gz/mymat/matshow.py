# -*- coding: utf-8 -*-
'''mymath.draw

-------------------------------
Path: mywork\mymat
Author: William/2016-04
'''

import matplotlib.pyplot as plt

import mymat


class MatrixShow:
    # myClass
    def __init__(self, matrix, axes=None, figure=plt.figure()):
        self.matrix = matrix
        if axes is None:
            self.figure = figure
            self.axes = figure.add_subplot(111)
        else:
            self.axes = axes
        self.text = None

    @property
    def size(self):
        return self.matrix.shape
        
    def show(self):
        # show matrix on an axes
        offset=0.5
        self.draw_grid()
        m, n = self.size
        self.text = [[self.axes.text(j-offset, m-i+offset, self.matrix[i,j]) for j in range(1, n+1)] for i in range(1, m+1)]
        plt.show()


    def set_text(self, i, j, v):
        self.text[i][j]._text = str(v)

    def draw_grid(self):
        m, n = self.size
        for k in range(m+1):
            self.axes.plot([0,n], [k,k])
        for l in range(n+1):
            self.axes.plot([l,l], [0,m])

if __name__ == "__main__":
    A = mymat.MyMat('1,2;3,5;4,6')
    ms = MatrixShow(A)
    ms.show()
