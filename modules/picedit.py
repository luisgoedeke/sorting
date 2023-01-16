import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import color
from skimage import io

#path='C:/Users/Luis/Pictures/rainbow.jpg'

#img = cv2.imread(path)

#plt.imshow(img)

#img = cv2.imread(path,0)

#cv2.imwrite('C:/Users/Luis/Pictures/rainbowblack.jpg',img)

#ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

#cv2.imwrite('C:/Users/Luis/Pictures/rainbowblack.jpg',thresh1)
 
#source = 'C:/Users/Luis/Pictures/Bilder'

#destination = 'C:/Users/Luis/Pictures/Bilder3'

#test=1

#for dir1 in os.listdir(source):
    #for dir2 in os.listdir(os.path.join(source, dir1)):
        #os.makedirs(os.path.join(destination, dir1,dir2))
        #for dir3 in os.listdir(os.path.join(source, dir1,dir2)):
            #path=os.path.join(source, dir1,dir2,dir3)
            #print(path)
            #pic=os.path.join(destination, dir1,dir2,dir3)
            #img = cv2.imread(path,0)
            #cv2.imwrite(pic,img)
            #print(test)
            #test=test+1

img = cv2.imread('C:/Users/Luis/Pictures/test.jpg')
img = img[0:480, 104:584]
gamma = 0.95
img = np.power(img, gamma)
imgGray = color.rgb2gray(img)
#image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#ret,img = cv2.threshold(img,150,255,cv2.THRESH_TRUNC)
cv2.imwrite('C:/Users/Luis/Pictures/test1.jpg',imgGray)
