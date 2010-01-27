#!/usr/bin/python

import sys
import math
#Qt GUI libraries
from PyQt4 import QtGui, QtCore

#OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4.QtOpenGL import *

class ViewerWidget(QGLWidget):
    """
    widget for viewing Stereo 3D
    #just testing with a simple spiral demo
    #need to refactor olmo's code to use this
    """
    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(500,500)

    def paintGL(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        radius = 1.0
        x = radius*math.sin(0)
        y = radius*math.cos(0)
        glColor(0.0, 1.0, 0.0)
        glBegin(GL_LINE_STRIP)
        for deg in xrange(1000):
            glVertex(x, y, 0.0)
            rad = math.radians(deg)
            radius -= 0.001
            x = radius*math.sin(rad)
            y = radius*math.cos(rad)
        glEnd()

        glEnableClientState(GL_VERTEX_ARRAY)

        glFlush()

    def resizeGL(self, w, h):
        glViewport(0,0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(4.0, 1.0, 1.0, 30.0)






class MPOEditor(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)
        self.setGeometry(500, 600, 400, 300)
        self.setWindowTitle('MPO editor - pys3d')

        button = QtGui.QPushButton('Pop', self)
        button.setGeometry(10, 10, 65, 30)
        self.connect(button, QtCore.SIGNAL('clicked()'),self.pop)

        widget = ViewerWidget(self)
        self.setCentralWidget(widget)



    def pop(self):
       reply = QtGui.QMessageBox.question(self, 'Pop',
            "Goes the weasel", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

       if reply == QtGui.QMessageBox.Yes:
            #event.accept()
            print "yes"
       else:
            #event.ignore() 
            print "no"

app = QtGui.QApplication(sys.argv)

mpoe = MPOEditor()
mpoe.show()

sys.exit(app.exec_())
