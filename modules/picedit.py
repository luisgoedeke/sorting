import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

#path='C:/Users/Luis/Pictures/rainbow.jpg'

#img = cv2.imread(path)

#plt.imshow(img)

#img = cv2.imread(path,0)

#cv2.imwrite('C:/Users/Luis/Pictures/rainbowblack.jpg',img)

#ret,thresh1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

#cv2.imwrite('C:/Users/Luis/Pictures/rainbowblack.jpg',thresh1)

import os 
source = 'C:/Users/Luis/Pictures/Bilder'

destination = 'C:/Users/Luis/Pictures/Bilder3'

test=1

#os.makedirs(destination))

for dir1 in os.listdir(source):
    #os.makedirs(os.listdir(os.path.join(destination, dir1)))
    for dir2 in os.listdir(os.path.join(source, dir1)):
        os.makedirs(os.path.join(destination, dir1,dir2))
        for dir3 in os.listdir(os.path.join(source, dir1,dir2)):
            path=os.path.join(source, dir1,dir2,dir3)
            print(path)
            pic=os.path.join(destination, dir1,dir2,dir3)
            img = cv2.imread(path,0)
            cv2.imwrite(pic,img)
            print(test)
            test=test+1   
