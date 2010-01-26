# helper class for stereo visualisation using OpenGL
# The underlying equations and their implementation are by courtesy of 
# Paul Bourke, http://local.wasp.uwa.edu.au/~pbourke/projection/stereorender/
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This code is licensed under the PyOpenGL License.
# Details are given in the file license.txt included in this distribution.


## Modified from the above original source code
## Below is a helper class for class parallel.py 
## a demonstration of stereo viewing in OpenGL using the
## parallel camera's approach

## August 2009, Peter Hughes, Durham University - Z0903068
## MSc Computer Science, Internet Systems and eBusiness

## Acknowledgements: Dr Nick Holliman Durham University


import sys
import math

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

class StereoCamera( object ):

    def update( self ):
            w = 2736 # Physical display dimensions in mm. (Width)
            h = 3638 # (Height)

            Z = 100.0 # Distance in the scene from the camera to the display plane.
            A = 0.0   # Camera inter-axial separation (eye separation).
            Near = 800.0  # Distance in the scene from the camera to the near plane.
            Far = 1200.0 # Distance in the scene from the camera to the far plane.


        # Calculations for Left eye/camera Frustum
            L_l =  -( Near * ( ( w/2.0 - A/2.0 )/ Z ) ) # left clipping pane
            L_r =  ( Near * ( ( w/2.0 + A/2.0 )/ Z ) ) # right clipping pane
            L_b = - ( Near * ( (h/2.0)/Z) ) # bottom clipping pane
            L_t =   ( Near * ( (h/2.0)/Z) ) # top clipping pane

        # Calculations for Right eye/camera Frustum
            R_l =  -( Near * ( ( w/2.0 + A/2.0 )/ Z ) ) # left clipping pane
            R_r =  ( Near * ( ( w/2.0 - A/2.0 )/ Z ) ) # right clipping pane
            R_b = - ( Near * ( (h/2.0)/Z) ) # bottom clipping pane
            R_t =   ( Near * ( (h/2.0)/Z) ) # top clipping pane

            leftposx=-300
            rightposx=300
            self.lookAtLeft = (
                    leftposx,0,0,leftposx,0,-Z,0,1,0)
                    #-A/2, 0, 0, -A/2, 0, -Z, 0, 1, 0 ) # Lookat points for left eye/camera

            self.lookAtRight = (
                    rightposx,0,0,rightposx,0,-Z,0,1,0)
                    #A/2, 0, 0, A/2, 0, -Z, 0, 1, 0 ) # Lookat points for right eye/camera

            self.frustumLeft = (
                    L_l, L_r, L_b, L_t, Near, Far ) # Parameters for glFrustum (Left)
            self.frustumRight = (
                    R_l, R_r, R_b, R_t, Near, Far ) # Parameters for glFrustum (Right)

# test program - when stereoCamera.py is run, will print values in lists (collection) for lookAt points and Frustum parameters
if __name__ == '__main__' :
	sC = StereoCamera( )		
	sC.update( )
	print sC.lookAtLeft
	print sC.frustumLeft
	print sC.lookAtRight
	print sC.frustumRight
