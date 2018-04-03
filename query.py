import urllib
import urllib.request
import numpy
import logging
import shutil
import cv2
import main as quad


base='http://h0.ortho.tiles.virtualearth.net/tiles/h'
end='.jpeg?g=131'

extra=quad.get_tile(41.832482, -87.615588)
print(extra)

url_string=base+extra+end
print(url_string)

file_name=extra+'.jpeg'

image=urllib.request.urlretrieve(url_string,file_name)


#print(image)
image1=cv2.imread(file_name)
cv2.imshow('image',image1)
cv2.waitKey(0)
cv2.destroyWindow('image')