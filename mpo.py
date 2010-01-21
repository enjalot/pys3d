import Image
import StringIO

im = Image.open("wescott.mpo")
print im.format, im.size, im.mode
#im.show()

f = open('wescott.mpo')
fr = f.read()
i = fr.find('\xff\xd8\xff\xe1',4)
#print i
xa = fr[0:i]
xb = fr[i:]

xas = StringIO.StringIO(xa)
xbs = StringIO.StringIO(xb)

#ima = Image.open(xas)
imb = Image.open(xbs)
imb.show()






