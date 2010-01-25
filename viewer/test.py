import Image
import OpenGL
import numpy

img = Image.open('random-90.jpg')
img_data = numpy.array(list(img.getdata()), numpy.int8)

texture = glGenTextures(1)
glPixelStorei(GL_UNPACK_ALIGNMENT,1)
glBindTexture(GL_TEXTURE_2D, texture)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)




