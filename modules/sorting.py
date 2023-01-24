import time
import datetime
import serial
import os
import numpy as np
import matplotlib.pyplot as plt
from skimage import color
import sys
import cv2                     
import RPi.GPIO as GPIO        
from machine import *
from lid import *
from datetime import date
machine = Machine()
import pathlib
import tflite_runtime.interpreter as tflite
import queue
from threading import Thread



class Sorting:
        
        #initialisierung der Queues und Variablen

        def __init__(self,m):
            self.q1 = queue.Queue()
            self.q2 = queue.Queue()
            self.q3 = queue.Queue()
            self.machine = m
            self.x = False
            pass

        #Hauptprogramm zur Vereinzelung

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

                            # Bild bearbeiten
                            while True:   

                                try:
                                    img = img[0:480, 104:584] #Bild zuschneiden
                                    break
                                except:
                                    img = self.machine.picture(number) #erneute Aufnahme



                            lab= cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
                            l_channel, a, b = cv2.split(lab)

                            clahe = cv2.createCLAHE(clipLimit=2.7, tileGridSize=(8,8))
                            cl = clahe.apply(l_channel)

                            limg = cv2.merge((cl,a,b))

                            enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

                            gamma = 0.95
                            img = np.power(enhanced_img, gamma)
                            img = color.rgb2gray(img)

                            cv2.imwrite('/home/pi/images/Aufnahmen/' + str(number) + '.jpg',img) #Bild speichern
                            print("Bild bearbeitet")
                            
                            # Deckel erkennen 

                            # Load TFLite model
                            interpreter = tflite.Interpreter(model_path="/home/pi/images/bilder bearbeitet/model.tflite")

                            # Get input and output tensors
                            input_details = interpreter.get_input_details()
                            output_details = interpreter.get_output_details()

                            interpreter.allocate_tensors()
                            
                            self.machine.delay(1)
                                
                            for file in pathlib.Path("/home/pi/images/Aufnahmen/").iterdir():
                                
                                # Bild einlesen
                                img = cv2.imread("/home/pi/images/Aufnahmen/"+ str(number)+ '.jpg'.format(file.resolve()))

                                #Auflösung ändern
                                new_img = cv2.resize(img, (224, 224))
                                
                                # input_details[0]['index'] = the index which accepts the input
                                interpreter.set_tensor(input_details[0]['index'], [new_img])
                                
                                # run the inference
                                interpreter.invoke()
                                
                                # output_details[0]['index'] = the index which provides the input
                                output_data = interpreter.get_tensor(output_details[0]['index']) 

                                print(output_data[0][0]/255*100,"% Kronkorken", output_data[0][1]/255*100,"% Metall", output_data[0][2]/255*100, "% Kunststoff")
                                
                                #Erstellung eines arrays zur Speicherung der Ergebnisse

                                klasse = (output_data[0][0], output_data[0][1], output_data[0][2], 0)

                                #Ab 70% Erkennung werden die Deckel der Queue zugeordnet
                                if klasse[0] > 180: # 180 entspricht ~70%
                                    self.q1.put(Kronkorken())
                                    
                                elif klasse[1] > 180: # 180 entspricht ~70%
                                    self.q1.put(Metall())
                                    
                                elif klasse[2] > 180: # 180 entspricht ~70%
                                    self.q1.put(Kunststoff())
                                    
                                else:
                                    self.q1.put(Ausschuss())
                                    
                                # Zylinder 3 ausfahren, wenn Klasse 0 zugeordnet
                                a = self.q1.get()
                                if a.get_pos_soll() == 1:
                                    self.machine.push_zyl_3()
                                    self.machine.delay(2)
                                    self.machine.pull_zyl_3()
                                    
                                else: 
                                    self.q2.put(a)
                                    self.machine.start_belt_rl()
                                    self.x = False
                                    self.ls2() #Methode der Lichtschranke 2
                                    if self.x:
                                        self.ls1() #Methode der Lichtschranke 1
                        
                                break
                            number = number +1

                            break                                    
                                                                  
        def ls2(self):

            while True:

                if machine.get_ls_2():
                    a = self.q2.get()
                        
                    if a.get_pos_soll()==2:

                        print("ls2 if schleife")
                        self.machine.push_zyl_2()
                        self.machine.delay(2)
                        self.machine.pull_zyl_2()
                        break
                    
                    else:
                        
                        self.x = True #x gleich True setzen um in ls1 zu springen
                        self.q3.put(a)
                        break
                    break
                        
                
        def ls1(self):

            while True:
                
                if machine.get_ls_1():
                    
                    b = self.q3.get()
                        
                    if b.get_pos_soll()==3:

                        self.machine.push_zyl_1()
                        self.machine.delay(2)
                        self.machine.pull_zyl_1()

                        break

                    break