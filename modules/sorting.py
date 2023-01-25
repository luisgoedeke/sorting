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
        self.z1 = 0 #Zählervariable Anzahl Deckel Behälter 3 (Anzahl Ausfahren Zylinder 1)
        self.z2 = 0 #Zählervariable Anzahl Deckel Behälter 2 (Anzahl Ausfahren Zylinder 2)
        self.z3 = 0 #Zählervariable Anzahl Deckel Behälter 2 (Anzahl Ausfahren Zylinder 3)
        self.zyl1 = 0
        self.zyl2 = 0
        self.zyl3 = 0
        self.sorting_allowed = True
        self.run_belt_allowed = False
        pass

    #Hauptprogramm zur Vereinzelung

    def classify(self):
        number  = 0
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

            # Das aufgenommene Bild wird klassifiziert

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
            classification = (output_data[0][0], output_data[0][1], output_data[0][2], 0)
            return classification

    def classify_threshold(self):
        number  = 0
        img = self.machine.picture(number) # Bild aufnehmen

        # Bild bearbeiten
        while True:

            try:
                img = img[0:480, 104:584] #Bild zuschneiden
                break
            except:
                img = self.machine.picture(number) #erneute Aufnahme



        img = cv2.medianBlur(img,5)


        #Das sind addaptive Methoden, die den optimalen Threshold selber finden 
        ret,th1 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
        th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        titles = ['Original Image', 'Global Thresholding (v = 127)', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']

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

        # Das aufgenommene Bild wird klassifiziert

        # Bild einlesen
        img = cv2.imread("/home/pi/images/Aufnahmen/"+ str(number)+ '.jpg'.format(file.resolve()))

        #Auflösung ändern
        #new_img = cv2.resize(img, (224, 224))

        # input_details[0]['index'] = the index which accepts the input
        interpreter.set_tensor(input_details[0]['index'], [img])

        # run the inference
        interpreter.invoke()

        # output_details[0]['index'] = the index which provides the input
        output_data = interpreter.get_tensor(output_details[0]['index'])

        print(output_data[0][0]/255*100,"% Kronkorken", output_data[0][1]/255*100,"% Metall", output_data[0][2]/255*100, "% Kunststoff")

        #Erstellung eines arrays zur Speicherung der Ergebnisse
        classification = (output_data[0][0], output_data[0][1], output_data[0][2], 0)
        return classification

    def sort(self):
            number = 0 #Zählervariable zur Benennung der Deckel

            while self.sorting_allowed:

                self.machine.start_belt_rl()
                self.machine.start_ver()

                while self.sorting_allowed:

                    if self.machine.get_ls_4(): # Ein Deckel ist aus der Vereinzelung gefallen
                        self.machine.stop_ver() # Die Vereinzelung hält an
                        break

                while self.sorting_allowed:

                    if self.machine.get_ls_3():     # Der Deckel hat die Kamera erreicht (Lichtschranke 3)
                        self.machine.stop_belt()    # Die Vereinzelung hält an
                        self.machine.delay(2)
                        

                        klasse = self.classify()

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
                        a = self.q1.get() # das älteste Element der Schlange q1 wird aus der Schlange genommen und in a gespeichert
                        if a.get_pos_soll() == 1:
                            self.machine.push_zyl_3()
                            self.zyl3 += 1
                            self.machine.delay(2)
                            self.machine.pull_zyl_3()

                        else:
                            self.q2.put(a) #Deckel wird in die nächste Schlange (q2) verschoben
                            self.machine.start_belt_rl()
                            self.x = False # Variable x wird auf false gesetzt (Default-Wert)
                            self.ls2() #Methode der Lichtschranke 2
                            if self.x: # Falls der Deckel in ls2() nicht vom Band geschoben wurde, ist x = True und ls1() wird durchlaufen
                                self.ls1() #Methode der Lichtschranke 1

                            break
                        number = number +1 # Hochzählen der Zählervariable zur Benennung der Deckel
                        # Ausgabe der Füllstände in den drei Behältern
                        print("Füllstände: Kronkorken:  " + str(self.zyl3))
                        print("            Metall:      " + str(self.zyl2))
                        print("            Kunststoff:  " + str(self.zyl1))

                        break

    def ls2(self): #Methode zum Ausfahren des Zylinders2 wenn Lichtschranke 2 triggert und es sich um einen Metalldeckel (=Sollposition 2) handelt

        while True:

            if machine.get_ls_2():

                b = self.q2.get() # das älteste Element der Schlange q2 wird aus der Schlange genommen und in b gespeichert

                if b.get_pos_soll()==2:

                    self.machine.push_zyl_2()
                    self.zyl2 += 1
                    self.machine.delay(2)
                    self.machine.pull_zyl_2()
                    break

                else:

                    self.x = True #x gleich True setzen um in ls1 zu springen
                    self.q3.put(b)
                    break
                break


    def ls1(self):  #Methode zum Ausfahren des Zylinders1 wenn Lichtschranke 1 triggert und es sich um einen Kunststoffdeckel (=Sollposition 3) handelt

        while True:

            if machine.get_ls_1():

                c = self.q3.get()  # das älteste Element der Schlange q3 wird aus der Schlange genommen und in c gespeichert

                if c.get_pos_soll()==3:

                    self.machine.push_zyl_1()
                    self.zyl1 += 1
                    self.machine.delay(2)
                    self.machine.pull_zyl_1()

                    break

                else:       # Deckel mit der Soll-Pos 4 (Ausschuss) werden nicht vom Band geschoben und gelangen am Ende des Bandes in den Ausschuss-Behälter

                    break

                break
