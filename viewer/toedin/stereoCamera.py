# helper class for stereo visualisation using OpenGL
# The underlying equations and their implementation are by courtesy of 
# Paul Bourke, http://local.wasp.uwa.edu.au/~pbourke/projection/stereorender/
# 
# Copyright (C) 2007  "Peter Roesch" <Peter.Roesch@fh-augsburg.de>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# or open http:#www.fsf.org/licensing/licenses/gpl.html


## Modified from the above original source code
## Below is a helper class for class toedin.py 
## a demonstration of stereo viewing in OpenGL using the
## toed-in or verging camera's approach

## August 2009, Peter Hughes, Durham University - Z0903068
## MSc Computer Science, Internet Systems and eBusiness

## Acknowledgements: Dr Nick Holliman Durham University


import sys
import math

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  import math
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

class StereoCamera( object ):
	

	
	def update( self ):
		w = 518.4 # Physical display dimensions in mm (Width)
		h = 324.0 # (Height)
		

		Z = 1000.0 # Distance in the scene from the camera to the display plane.
		A = 65.0   # Camera inter-axial separation (eye separation).
		Near = 800.0  # Distance in the scene from the camera to the near plane.
		Far = 1200.0 # Distance in the scene from the camera to the far plane.

		half_fov = math.atan( (h/2.0) / Z )
		fov = math.degrees( 2.0 * half_fov ) # field of view (fov) in y (vertical axis) direction.

		
		self.lookAtLeft = ( 
			-A/2, 0, 0, 0, 0, -Z, 0, 1, 0 ) # Lookat points for left eye/camera
		self.lookAtRight = ( 
			A/2, 0, 0, 0, 0, -Z, 0, 1, 0 ) # Lookat points for right eye/camera
		
		self.gluPerspective = ( fov, w/h, Near, Far ) # Parameters for gluPerspective (Left and Right)

		
		

# test program - when stereoCamera.py is run, will print values in lists (collection) for lookAt points and gluPerspective parameters
if __name__ == '__main__' :
	sC = StereoCamera( )

	
	sC.update( )
	print sC.lookAtLeft
	print sC.lookAtRight
	print sC.gluPerspective
      