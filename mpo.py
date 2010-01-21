import Image
import StringIO
import mmap

#split an MPO file object and return left and right Image objects
def split_mpo(file):
    filestr = file.read()
    #find the JPEG Start of Image Marker
    #need to start at 4, so that it doesn't find the first image
    ind = filestr.find('\xff\xd8\xff\xe1',4) 

    fls = filestr[0:ind]
    frs = filestr[ind:]
    
    fleft = StringIO.StringIO(fls)
    fright = StringIO.StringIO(frs)

    return Image.open(fleft), Image.open(fright), [len(fls), len(frs)]


#rotate a pair of images counter-clockwise
def rotate_pair(fleft, fright, degrees):
    degrees = -degrees
    imlrot = fleft.rotate(degrees)
    imrrot = fright.rotate(degrees)
   
    return imlrot, imrrot

#Merge left and right Image objects into a file
def merge_to_mpo(fl, fr, size):
    #make in-memory files so Image module can write to them
    lmap = mmap.mmap(-1, size[0])
    rmap = mmap.mmap(-1, size[1])
    fl.save(lmap, 'JPEG')
    fr.save(rmap, 'JPEG')
    #gotta seek back to 0 so we can write out to a file
    lmap.seek(0)
    rmap.seek(0)
   
   """
    flo = open("testleft.jpg", 'w')
    flo.write(lmap.read(size[0]))
    flo.close()
    """
    
    #append the images together
    mpo = lmap.read(size[0]) + rmap.read(size[1])
    fmpo = open("test.mpo", 'wb')
    fmpo.write(mpo)
    fmpo.close()
    


f = open('../sistersstatue.mpo')
fl, fr, size = split_mpo(f)
fl, fr = rotate_pair(fl, fr, 90)
merge_to_mpo(fl, fr, size)
