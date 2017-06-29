# -*- coding: utf-8 -*-
"""
copyright 2016-2017 Dan Aukes
"""
import PyQt5.QtGui as qg
import pyqtgraph.opengl as pgo
import sys

def plot_mi(mi):
    app = qg.QApplication(sys.argv)
    w = pgo.GLViewWidget()    
    w.addItem(mi)
    w.show()
    sys.exit(app.exec_())


def plot_tris(verts,tris,verts_colors = None,face_colors = None):

    
    md = pgo.MeshData(vertexes = verts,faces = tris,vertexColors = verts_colors,faceColors = face_colors)
    mi = pgo.GLMeshItem(meshdata = md,shader='balloon',drawEdges=False,edgeColor = [1,1,1,1],smooth=False,computeNormals = False,glOptions='opaque')
#    mi = pgo.GLMeshItem(meshdata = md,shader='shaded',drawEdges=False,smooth=True,computeNormals = True,glOptions='opaque')
    
    plot_mi(mi)
if __name__=='__main__':
    import numpy
    verts = []
    verts.append([0,0,0])
    verts.append([1,0,0])
    verts.append([0,1,0])
    verts.append([0,0,1])
    verts = numpy.array(verts)
    
    verts_colors = []
    verts_colors.append([1,1,1,1])
    verts_colors.append([1,0,0,1])
    verts_colors.append([0,1,0,1])
    verts_colors.append([0,0,1,1])
    verts_colors = numpy.array(verts_colors)
    
    tris = []
    tris.append([0,1,2])
    tris.append([1,2,3])
    tris.append([2,3,0])
    tris.append([3,0,1])
    tris = numpy.array(tris)
    
    plot_tris(verts,tris,verts_colors)
