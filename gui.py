#!/usr/bin/python

import sys
from PyQt4 import QtGui, QtCore

def asdf():
    print "asdf"

class MPOEditor(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('MPO editor - pys3d')

        button = QtGui.QPushButton('Pop', self)
        button.setGeometry(10, 10, 65, 30)

        self.connect(button, QtCore.SIGNAL('clicked()'),
            self.pop)


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
