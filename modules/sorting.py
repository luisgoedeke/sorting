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
from lid import *
from datetime import date
machine = Machine()
import pathlib
import tflite_runtime.interpreter as tflite
import queue
from threading import Thread


# Anlegen eines Ordners mit Datum + Uhrzeit als Benennung
#datestring = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#print (datestring)
#os.mkdir('/home/pi/' + datestring)
#os.mkdir(r"C:\Diesen\Pfad\gibt\es\so\noch\nicht")

# Index als Benennung der Deckel

    
class Sorting:
        
        def __init__(self,m):
            self.q1 = queue.Queue()
            self.q2 = queue.Queue()
            self.q3 = queue.Queue()
            self.machine = m
            print("Konst")
            pass
        
        def sort(self):
                number = 0
               
                
                
                while True:
                    
                    self.machine.start_belt_rl()

                    self.machine.start_ver()

                    while True:
                        if self.machine.get_ls_4():
                            self.machine.stop_ver()
                            break

                    while True:
                        if self.machine.get_ls_3():
                            self.machine.stop_belt()
                            self.machine.delay(2)
                            img = self.machine.picture(number) # Bild aufnehmen
                            
                            self.machine.delay(3)
                            # Bild bearbeiten
                            while True:
                                try:
                                    img = img[0:480, 104:584] #Bild zuschneiden
                                    break
                                except:
                                    img = self.machine.picture(number)
                                    #img = img[0:480, 104:584]

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
                            
                            
                            self.machine.delay(1)
                                
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
                                
                                klasse = (output_data[0][0], output_data[0][1], output_data[0][2], 0)
                                
                         
                                
                                # Werte auf 0 und 1 bringen
                                if klasse[0] > 180: # 180 entspricht ~70%
                                    #klasse=(1,0,0,0)

                                    self.q1.put(Kronkorken())
                                   
                                    
                                elif klasse[1] > 180: # 180 entspricht ~70%
                                    self.q1.put(Metall())
                                    
                                
                                    
                                elif klasse[2] > 180: # 180 entspricht ~70%
                                    self.q1.put(Kunststoff())
                                    
                                else:
                                    self.q1.put(Ausschuss()) # Klasse 4 (Ausschuss) zuordnen, falls keiner der drei Klassen größer 70%
                                    
                                # Zylinder 3 ausfahren, wenn Klasse 0 zugeordnet
                                a = self.q1.get()
                                if a.get_pos_soll() == 1:
                                    self.machine.push_zyl_3()
                                    self.machine.delay(2)
                                    self.machine.pull_zyl_3()
                                    
                                else:
                                    self.q2.put(a)
                                    
                                break
                            
                            
                            #machine.delay(5)
                            number = number +1

                            break                                    
                                    
                                    
        def ls2(self):
            nummerls2 = 0
            while True:
                
                if machine.get_ls_2():
                    a = self.q1.get()
                    
                    if a.get_pos_soll()==2:
                        self.machine.push_zyl_2()
                        self.time.sleep(2)
                        self.machine.pull_zyl_2()
                    else:
                        q2.put(a)
                        
                #print("ls2 durchgelaufen")
                time.sleep(0.1)
                nummerls2 = nummerls2 + 1
                print("Nummerls2= " + str(nummerls2))
                        
                
        def ls1(self):
            nummerls1 = 0
            while True:
               
                if self.machine.get_ls_1():
                    
                    c = self.q3.get()
                    
                    if c.get_pos_soll() == 3:
                        self.machine.push_zyl_1()
                        self.machine.delay(2)
                        self.machine.pull_zyl_1()
                    
                #print("ls1 durchgelaufen")
                time.sleep(0.1)
                nummerls1 = nummerls1 + 1
                print("Nummerls1= " + str(nummerls1))
                        
        def start(self):
            thread_1 = Thread(target=self.sort)
            thread_2 = Thread(target=self.ls2)
            thread_3 = Thread(target=self.ls1)
            
            thread_1.start()
            thread_2.start()
            thread_3.start()

