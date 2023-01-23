import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
 
source = 'C:/Users/Luis/Pictures/Bilder'

destination = 'C:/Users/Luis/Pictures/Bilder_bearbeitet'

test=1

for dir1 in os.listdir(source):
    for dir2 in os.listdir(os.path.join(source, dir1)):
        os.makedirs(os.path.join(destination, dir1,dir2))
        for dir3 in os.listdir(os.path.join(source, dir1,dir2)):
            spath=os.path.join(source, dir1,dir2,dir3) #Quellpfad
            print(spath)
            dpath=os.path.join(destination, dir1,dir2,dir3) #Zielpfad
            img = cv2.imread(spath) #Bild einlesen
            img = img[0:480, 104:584] #Bild zuschneiden

            lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
            l_channel, a, b = cv2.split(lab)

            # Applying CLAHE to L-channel
            # feel free to try different values for the limit and grid size:
            clahe = cv2.createCLAHE(clipLimit=2.7, tileGridSize=(8,8))
            cl = clahe.apply(l_channel)

            # merge the CLAHE enhanced L-channel with the a and b channel
            limg = cv2.merge((cl,a,b))

            # Converting image from LAB Color model to BGR color spcae
            enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

            #Geliehen von https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv


            gamma = 0.95
            img = np.power(enhanced_img, gamma)
            imgGray = color.rgb2gray(img)
            cv2.imwrite(dpath,imgGray)

            print(test)
            test=test+1

