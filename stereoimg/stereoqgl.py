#!/usr/bin/python
import sys
import math
#Qt GUI libraries
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PIL.ImageQt import QImage
from PyQt4.QtOpenGL import *

#OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from time import sleep
"""TODO 
    Test SHUTTER
    Test updateGL as a public slot
    Timer to re draw the scene. Do the resize method.
    Modify the size of the widget somehow
"""

class ViewerWidget(QGLWidget):
    """
    Widget for viewing Stereo 3D
    """
    def __init__(self, parent):
        self.textures = [0, 1]#Textures ids
        self.stereoMode = "ANAGLYPH" #Stereo mode ("ANAGLYPH, SHUTTER, NONE)
        self.lightColors = {
            "white":(1.0, 1.0, 1.0, 1.0),
            "red":(1.0, 0.0, 0.0, 1.0),
            "green":(0.0, 1.0, 0.0, 1.0),
            "blue":(0.0, 0.0, 1.0, 1.0)
        }        
        QGLWidget.__init__(self, parent)

    def mousePressEvent(self,mouseEvent):
        "Get the mouse events, in this case used to change image"
        self.loadImages("images/sistersleft.bmp","images/sistersright.bmp")#Loads stereo images
        self.loadTextures()#Applies images as billboards in left right cameras        
        self.paintGL()
        print "Mouse at:",mouseEvent.x(),",",mouseEvent.y()
        
    def updateGL(self):
        """Updates the display. Its a public slot"""        
        self.paintGL()

    def paintGL(self):
        """Main function to render objects in OpenGL"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)        
        self.display()#Render the stereo images

    def resizeGL(self, w, h):
        """
        Called when the widget is resized.
        TODO Resize everything to fit the screen
        """        
        glViewport(0,0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, 1.0, 1.0, 30.0)

    def initializeGL(self):
        """
        Initialize all the OpenGL paramaters
        TODO. Set the initial size of the widget from other place
        maybe the size of the monitor, the parent window etc.
        """
        glClearColor(0.0, 0.0, 0.0, 1.0)#Black background                
        glEnable(GL_TEXTURE_2D);#Enable texturing
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()        

        self.loadImages("images/leftImage.jpg","images/rightImage.jpg")#Loads stereo images
        self.loadTextures()#Applies images as billboards in left right cameras    
        self.setMinimumSize(self.imw,self.imh)
        self.setAutoBufferSwap(0)# Stoping auto buffering for stereo        

    def loadImages(self,leftImFile,rightImFile):
        """
        Loads two images with equal dimensions into the left and right eye
        """
        self.image_left = QImage()
        self.image_right= QImage()

        self.image_left.load(QString(leftImFile))
        self.image_right.load(QString(rightImFile))
        
        #Verify the two images are of equal size
        if( (self.image_left.width()!=self.image_right.width()) or
            (self.image_left.height()!=self.image_right.height()) ):
            print "Both imager needs to have the same size"
        
        temp_imw = self.image_left.width()
        temp_imh = self.image_right.height()        
        #Initial with of the image 1024
        if(temp_imw>temp_imh):
            self.imw = 1024
            self.imh = int(self.imw*(float(temp_imh)/float(temp_imw)))
        else:
            self.imh = 768
            self.imw = int(self.imh*(float(temp_imw)/float(temp_imh)))


    def loadTextures(self):
        """Loads the stereo images as textures"""
        self.textures[0] = self.bindTexture(self.image_left,
                                  GL_TEXTURE_2D)
        self.textures[1] = self.bindTexture(self.image_right,
                                  GL_TEXTURE_2D)

    def render(self, side):
        """
        Render the scene. It displays the right or the left images depending
        of the side parameter which can be: GL_BACK_LEFT or GL_BACK_RIGHT
        """
        imw, imh = [self.imw, self.imh]#Set image size as local variables

        if side == GL_BACK_LEFT: 
            l = [-imw/2,0,0,-imw/2,0,-10,0,1,0]#Position of the left camera
        else:
            l = [imw/2,0,0,imw/2,0,-10,0,1,0]#Position of the right camera

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        hnear = 10
        # This formula is straight forward from http://www.lighthouse3d.com/opengl/viewfrustum/index.php?defvf
        param1 = float(imh)/float(2*(hnear))
        param2 = math.degrees(math.atan(param1))
        gluPerspective(param2*2, float(imw)/float(imh), 10,1000)
        # collect lookAt parameters from stereoCamera.py
        gluLookAt( l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8] )

        #Distance of the images
        zdistance = -10

        glPushMatrix()
        if side == GL_BACK_LEFT:
            #Renders left image            
            glBindTexture(GL_TEXTURE_2D, self.textures[0])
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(-imw, -imh/2,  zdistance)    # Bottom Left Of The Texture and Quad
            glTexCoord2f(1.0, 0.0); glVertex3f(0, -imh/2,  zdistance)    # Bottom Right Of The Texture and Quad
            glTexCoord2f(1.0, 1.0); glVertex3f(0,  imh/2,  zdistance)    # Top Right Of The Texture and Quad
            glTexCoord2f(0.0, 1.0); glVertex3f(-imw,  imh/2,  zdistance)    # Top Left Of The Texture and Quad
            glEnd()
        else:
            #Renders right image
            glBindTexture(GL_TEXTURE_2D, self.textures[1])
            glBegin(GL_QUADS)
            glTexCoord2f(0.0, 0.0); glVertex3f(0, -imh/2,  zdistance)    # Bottom Left Of The Texture and Quad
            glTexCoord2f(1.0, 0.0); glVertex3f(imw, -imh/2,  zdistance)    # Bottom Right Of The Texture and Quad
            glTexCoord2f(1.0, 1.0); glVertex3f(imw,  imh/2,  zdistance)    # Top Right Of The Texture and Quad
            glTexCoord2f(0.0, 1.0); glVertex3f(0,  imh/2,  zdistance)    # Top Left Of The Texture and Quad
            glEnd()

        glPopMatrix()

    def setLightColor(self, s):
        """Set light color to 'white', 'red', 'green' or 'blue'."""
        if self.lightColors.has_key( s ):
         c = self.lightColors[ s ]
         glLightfv( GL_LIGHT0, GL_AMBIENT, c )
         glLightfv( GL_LIGHT0, GL_DIFFUSE, c )
         glLightfv( GL_LIGHT0, GL_SPECULAR, c )

    def display(self): # display relevant view - SHUTTER (true stereo, quad buffered), ANAGLYPH, or NONE (Monoscopic)
        """Glut display function."""
        if self.stereoMode != "SHUTTER":
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.stereoMode == "SHUTTER": # requires Quad Buffered Hardware
            #Buffer the left image
            glDrawBuffer( GL_BACK_LEFT )
            glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )#Clear
            self.render( GL_BACK_LEFT )#Render

            #Buffer the right image
            glDrawBuffer( GL_BACK_RIGHT )
            glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )#clear
            self.render( GL_BACK_RIGHT )#Render

        elif self.stereoMode == "ANAGLYPH": # red/green glasses viewing mode
            #Buffer left image
            glDrawBuffer( GL_BACK_LEFT )
            glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )#Clear
#            glColorMask( True, True, True, True )
            glColorMask( False, False, True, False )#Display only the blue comp.
            self.render( GL_BACK_LEFT )#Render

            glClear( GL_DEPTH_BUFFER_BIT )#Only clears the second buffer
            glColorMask( True, False, False, False)#Displ only the red comp
            self.render( GL_BACK_RIGHT )

            #Reset to write all components in the frame buffer
            glColorMask( True, True, True, True )
            self.swapBuffers()

        else: # monoscopic (draws left eye view only)
            glDrawBuffer(GL_BACK_LEFT)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.setLightColor( "white" )
            self.render(GL_BACK_LEFT)#We are only displaying the left image

class MPOEditor(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)        
        self.setWindowTitle('MPO editor - pys3d')

        widget = ViewerWidget(self)
        self.setCentralWidget(widget)

app = QtGui.QApplication(sys.argv)

mpoe = MPOEditor()
mpoe.show()

sys.exit(app.exec_())