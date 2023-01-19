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
from machine import *
from datetime import date
machine = Machine()
import pathlib
import tflite_runtime.interpreter as tflite


# Anlegen eines Ordners mit Datum + Uhrzeit als Benennung
#datestring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print (datestring)
#os.mkdir('/home/pi/' + datestring)
#os.mkdir(r"C:\Diesen\Pfad\gibt\es\so\noch\nicht")

# Index als Benennung der Deckel

class Sorting:
        def sort(self):
                machine = Machine()
                number = 0
                while True:
                    machine.start_belt_rl()

                    machine.start_ver()

                    while True:
                        if machine.get_ls_4():
                            machine.stop_ver()
                            break

                    while True:
                        if machine.get_ls_3():
                            machine.stop_belt()
                            #machine.delay(2)
                            img = machine.picture(number) # Bild aufnehmen
                            

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
                            cv2.imwrite('/home/pi/images/Aufnahmen/' + str(number) + '.jpg',img)
                            print("Bild bearbeitet")
                            
                       
                            
                            # Deckel erkennen

                            # Load TFLite model and allocate tensors.
                            interpreter = tflite.Interpreter(model_path="/home/pi/images/bilder bearbeitet/model.tflite")

                            # Get input and output tensors.
                            input_details = interpreter.get_input_details()
                            output_details = interpreter.get_output_details()

                            interpreter.allocate_tensors()

                            # input details
                            #print(input_details)
                            # output details
                            #print(output_details)
                            
                            
                            machine.delay(1)
                                
                            for file in pathlib.Path("/home/pi/images/Aufnahmen/").iterdir():
                                
                                # read and resize the image
                                img = cv2.imread("/home/pi/images/Aufnahmen/"+ str(number)+ '.jpg'.format(file.resolve()))
                                #print(img.shape)
                                new_img = cv2.resize(img, (224, 224))
                                
                                # input_details[0]['index'] = the index which accepts the input
                                interpreter.set_tensor(input_details[0]['index'], [new_img])
                                
                                # run the inference
                                interpreter.invoke()
                                
                                # output_details[0]['index'] = the index which provides the input
                                output_data = interpreter.get_tensor(output_details[0]['index']) 
                                
                                #print("For file {}, the output is {}".format(file.stem, output_data))
                                #print(output_data)
                                print(output_data[0][0]/255*100,"% Kronkorken", output_data[0][1]/255*100,"% Metall", output_data[0][2]/255*100, "% Kunststoff")

                                break
                            #machine.delay(5)
                            number = number +1

                            break
