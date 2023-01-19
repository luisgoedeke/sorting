import time
import datetime
import serial
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
import sys
import cv2                     #Bibliothek zum ansprechen der Kamera (Opencv)
import RPi.GPIO as GPIO        #Biblitheke, um die GPIO Pine per Programm ansprechen/auslesen zu können.
sys.path.insert(0, './modules')
from machine import *
from datetime import date
machine = Machine()


# Anlegen eines Ordners mit Datum + Uhrzeit als Benennung
#datestring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print (datestring)
#os.mkdir('/home/pi/' + datestring)
#os.mkdir(r"C:\Diesen\Pfad\gibt\es\so\noch\nicht")

# Index als Benennung der Deckel
index = 0

machine.start_belt_rl()

machine.start_ver()

while True:
    if machine.get_ls_4():
        machine.stop_ver()
        break

while True:
    if machine.get_ls_3():
        machine.stop_belt()
        machine.delay(2)
        img = machine.picture(index) # Bild aufnehmen
        

        # Bild bearbeiten
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
        img = color.rgb2gray(img)
        cv2.imwrite('/home/pi/images/' + str(index) + '.jpg',img)
        print("Bild bearbeitet")



        index = index +1

        break
