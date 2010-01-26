
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
  from Image import *
  import math
except:
  print ''' Error: PyOpenGL not installed properly !!'''
  sys.exit(  )

from stereoCamera import StereoCamera
sC = StereoCamera( )

animationAngle = 0.0
frameRate = 20
stereoMode = "ANAGLYPH"
lightColors = {
    "white":(1.0, 1.0, 1.0, 1.0),
    "red":(1.0, 0.0, 0.0, 1.0),
    "green":(0.0, 1.0, 0.0, 1.0),
    "blue":(0.0, 0.0, 1.0, 1.0)
}

lightPosition = (1.0, 5.0, 20.0, 1.0)

texture = 0
def loadImages():
    global imw, imh, image_left, image_right
    image_left = open("images/sistersleft.bmp")
    image_right = open("images/sistersright.bmp")

    temp_imw = image_left.size[0]
    temp_imh = image_left.size[1]

    if( (temp_imw!=image_right.size[0]) or
        (temp_imh!=image_right.size[1]) ):
        print "Not same size"

    if(temp_imw>temp_imh):
        imw = 1024
        imh = int(imw*(float(temp_imh)/float(temp_imw)))
    else:
        imh = 768
        imw = int(imh*(float(temp_imw)/float(temp_imh)))

def loadTextures():
    global textures, image_left,image_right

    temp_imw = image_left.size[0]
    temp_imh = image_left.size[1]

    image_left = image_left.tostring("raw", "RGBX", 0, -1)
    image_right = image_right.tostring("raw", "RGBX", 0, -1)

    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    textures = glGenTextures(2)

    glBindTexture(GL_TEXTURE_2D, textures[0])
    glTexImage2D(GL_TEXTURE_2D, 0, 3, temp_imw, temp_imh, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_left)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glBindTexture(GL_TEXTURE_2D, textures[1])
    glTexImage2D(GL_TEXTURE_2D, 0, 3, temp_imw, temp_imh, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_right)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

from time import sleep
def animationStep( ): # Setting abimation for centre cube under rotation
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
    glViewport( 0, 0, imw , imh)

    if side == GL_BACK_LEFT: # render left frustum and lookAt points
        l = [-imw/2,0,0,-imw/2,0,-10,0,1,0]
    else: # render right side view
        l = [imw/2,0,0,imw/2,0,-10,0,1,0]

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    hnear = 10
    # This formula is straight forward from http://www.lighthouse3d.com/opengl/viewfrustum/index.php?defvf
    param1 = float(imh)/float(2*(hnear))
    param2 = math.degrees(math.atan(param1))    
    gluPerspective(param2*2, float(imw)/float(imh), 10,1000)    
    gluLookAt( l[0], l[1], l[2], l[3], l[4], l[5], l[6], l[7], l[8] ) # collect lookAt parameters from stereoCamera.py

    # draw array of cubes at varying positions across scree
    zdistance = -10
    
    glPushMatrix()      
    glBindTexture(GL_TEXTURE_2D, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(-imw, -imh/2,  zdistance)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(0, -imh/2,  zdistance)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(0,  imh/2,  zdistance)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-imw,  imh/2,  zdistance)    # Top Left Of The Texture and Quad
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 2)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0); glVertex3f(0, -imh/2,  zdistance)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(imw, -imh/2,  zdistance)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(imw,  imh/2,  zdistance)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(0,  imh/2,  zdistance)    # Top Left Of The Texture and Quad
    glEnd()
    glPopMatrix()


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
    loadTextures()
    glEnable(GL_TEXTURE_2D)
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

#Here starts what should be the ---------------------------- MAIN ---------------------------
#If I put this inside a functions it doesnt work, I am dooing something wrong
glutInit( "" )
if stereoMode == "SHUTTER":
    #Options DisplayMode: GLUT_RGBA(default) GLUT_INDEX GLUT_RGB GLUT_SINGLE GLUT_DOUBLE GLUT_ACCUM GLUT_ALPHA GLUT_DEPTH GLUT_STENCIL GLUT_STEREO
    # GLUT_MULTISAMPLE GLUT_LUMINANCE
    glutInitDisplayMode( GLUT_STEREO | GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
else:
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH )
    
loadImages()
print "Size= ",imw,"x",imh

glutInitWindowSize(imw,imh)
    
glutInitWindowPosition( 300, 10)
glutCreateWindow( "3D pictures" )
init(  )

glutDisplayFunc( display )
glutIdleFunc( animationStep )
glutMainLoop(  )
