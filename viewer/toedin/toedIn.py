#!/usr/bin/python2.4
# OpenGL stereo demo using stereoCamera class
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


## Modified from the original source code
## Below is a demonstration of stereo viewing, implementing
## the toed-in (verging) camera setup (parameters of which are 
## obtained by helper class stereoCamera.py)

## August 2009, Peter Hughes, Durham University - Z0903068
## MSc Computer Science, Internet Systems and eBusiness

## Acknowledgements: Dr Nick Holliman Durham University



from sys import argv, exit
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  import math
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

from stereoCamera import StereoCamera
sC = StereoCamera( )

animationAngle = 0.0
frameRate = 20
stereoMode = "NONE"
lightColors = {
	"white":(1.0, 1.0, 1.0, 1.0),
	"red":(1.0, 0.0, 0.0, 1.0),
	"green":(0.0, 1.0, 0.0, 1.0),
	"blue":(0.0, 0.0, 1.0, 1.0)
}

lightPosition = (5.0, 5.0, 20.0, 1.0)

from time import sleep
def animationStep( ):
	"""Update animated parameters."""
	global animationAngle
	global frameRate
	animationAngle += 2
	while animationAngle > 360:
		animationAngle -= 360
	sleep( 1 / float( frameRate ) )
	glutPostRedisplay( )

def setLightColor( s ):
	"""Set light color to 'white', 'red', 'green' or 'blue'."""
	if lightColors.has_key( s ):
		c = lightColors[ s ]
		glLightfv( GL_LIGHT0, GL_AMBIENT, c )
		glLightfv( GL_LIGHT0, GL_DIFFUSE, c )
		glLightfv( GL_LIGHT0, GL_SPECULAR, c )

def render( side ):
	"""Render scene in either GLU_BACK_LEFT or GLU_BACK_RIGHT buffer"""
	boxSize = 50 # size of cube height, width and depth = 50mm
	separate = 100 # separation for array of cubes 100mm
	glViewport( 0, 0,
		glutGet( GLUT_WINDOW_WIDTH ), glutGet( GLUT_WINDOW_HEIGHT ))
	if side == GL_BACK_LEFT: # render left gluPerspective and lookAt points
		g = sC.gluPerspective 
		l = sC.lookAtLeft
	else: # render right side view
		g = sC.gluPerspective 
		l = sC.lookAtRight
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective( g[0], g[1], g[2], g[3] ) # collect parameters from stereoCamera.py for gluPerspective
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt( l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8] ) # collect lookAt parameters from stereoCamera.py
	
	
  # draw array of cubes at varying positions across screen
  	glPushMatrix();
   	glTranslatef( -separate, 0.0, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( 0.0, 0.0, -900 ); # draws centre cube - 100mm depth difference
   	glRotatef( animationAngle, 0.2, 0.7, 0.3 ) # rotates the cube
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate, 0.0, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();


	glPushMatrix();
   	glTranslatef( -separate, separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( 0.0, separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate, separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( -separate, -separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( 0.0, -separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate, -separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate*2, separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate*2, 0.0, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( separate*2, -separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();


	glPushMatrix();
   	glTranslatef( -separate*2, separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( -separate*2, 0.0, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();

	glPushMatrix();
   	glTranslatef( -separate*2, -separate, -1000 );
   	glutSolidCube( boxSize );
   	glPopMatrix();



def display(  ): # display relevant view - SHUTTER (true stereo, quad buffered), ANAGLYPH, or NONE (Monoscopic)
	"""Glut display function."""
	if stereoMode != "SHUTTER":
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	if stereoMode == "SHUTTER": # requires Quad Buffered Hardware
		setLightColor( "white" )
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_LEFT )
		glDrawBuffer( GL_BACK_RIGHT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		render( GL_BACK_RIGHT )
	elif stereoMode == "ANAGLYPH": # red/green glasses viewing mode
		glDrawBuffer( GL_BACK_LEFT )
		glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
		setLightColor( "red" )
		render( GL_BACK_LEFT )
		glClear( GL_DEPTH_BUFFER_BIT )
		glColorMask( False, True, False, False )
		setLightColor( "green" )
		render( GL_BACK_RIGHT )
		glColorMask( True, True, True, True )
	else: # monoscopic (draws left eye view only)
		glDrawBuffer(GL_BACK_LEFT)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		setLightColor( "white" )
		render(GL_BACK_LEFT)
	glutSwapBuffers( )

def init(  ): # OpenGL functions setting light, colour, texture etc
	"""Glut init function."""
	glClearColor ( 0, 0, 0, 0 )
	glEnable( GL_DEPTH_TEST )
	glShadeModel( GL_SMOOTH )
	glEnable( GL_LIGHTING )
	glEnable( GL_LIGHT0 )
	glLightModeli( GL_LIGHT_MODEL_TWO_SIDE, 0 )
	glLightfv( GL_LIGHT0, GL_POSITION, [4, 4, 4, 1] )
	lA = 0.8
	glLightfv( GL_LIGHT0, GL_AMBIENT, [lA, lA, lA, 1] )
	lD = 1
	glLightfv( GL_LIGHT0, GL_DIFFUSE, [lD, lD, lD, 1] )
	lS = 1
	glLightfv( GL_LIGHT0, GL_SPECULAR, [lS, lS, lS, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_AMBIENT, [0.2, 0.2, 0.2, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_DIFFUSE, [0.7, 0.7, 0.7, 1] )
	glMaterialfv( GL_FRONT_AND_BACK, GL_SPECULAR, [0.5, 0.5, 0.5, 1] )
	glMaterialf( GL_FRONT_AND_BACK, GL_SHININESS, 50 )
	sC.update( )


if len( argv ) != 2: # checks for at least 2 arguments to initiate program 
	print "Please choose viewing mode:"
	print "python toedin.py SHUTTER | ANAGLYPH | NONE \n"
else:
	glutInit( sys.argv )
	stereoMode = sys.argv[1].upper( )
	if stereoMode == "SHUTTER":
		glutInitDisplayMode( GLUT_STEREO | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
	else:
		glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
	glutInitWindowSize( 800, 600 )
	glutInitWindowPosition( 100, 100 )
	glutCreateWindow( sys.argv[0] )
	init(  )
	glutDisplayFunc( display )
	
	glutIdleFunc( animationStep )
	glutMainLoop(  )