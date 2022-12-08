#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Import von notwendigen Biblitheken
import time
import cv2
import RPi.GPIO as GPIO        #Biblitheke, um die GPIO Pine per Programm ansprechen/auslesen zu können.
from machine import Machine


#########################################################################################################
#Grundeinstellungen für die GPIOs

#GPIO.setmode(GPIO.BOARD)  #legt fest, wie die GPIO Pine im nachfolgenden Programm benannt werden müssen
#GPIO.setwarnings(False)   # Warnungen werden unterdrückt
#########################################################################################################

# Inputs
# GPIO Pins werden entsprechende Variablen zuweisen

#K1 = 23   #Lichtschranke 1 -> 1S1E
#K2 = 24   #Lichtschranke 2 -> 2S1E
#K3 = 7    #Lichtschranke 3 -> 3S1E
#K4 = 8    #Endlagensensor Zylinder 1 -> 1S2
#K5 = 10   #Endlagensensor Zylinder 2 -> 2S2
#K6 = 11   #Endlagensensor Zylinder 3 -> 3S2

#Die jeweiligen Pins als Input zuweisen, außerdem softwaremaessige Verwendung der internern Pull-Down Widerstaende

#GPIO.setup(K1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(K2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(K3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(K4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(K5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(K6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Outputs
# GPIO Pins werden entsprechende Variablen zuweisen

#K9 =  12    #Relais  K9 wird über den GPIO12 angsteuert.
#K10 = 13    #Relais K10 wird über den GPIO13 angsteuert.
#K11 = 15    #Relais k11 wird über den GPIO15 angsteuert.
#K12 = 16    #Relais K12 wird über den GPIO16 angsteuert.
#K13 = 18    #Relais K13 wird über den GPIO18 angsteuert.
#K14 = 19    #Relais K14 wird über den GPIO19 angsteuert.

#Die jeweiligen Pins als Output festlegen

#GPIO.setup(K9,  GPIO.OUT)       #schaltet 5/2 Wegventil -> 1Y1
#GPIO.setup(K10, GPIO.OUT)       #chaltet 5/2 Wegventil -> 1Y2
#GPIO.setup(K11, GPIO.OUT)       #schaltet 5/2 Wegeventil mit Federrückstellung -> 2Y1
#GPIO.setup(K12, GPIO.OUT)       #schaltet 5/2 Wegeventil mit Federrückstellung -> 3Y1
#GPIO.setup(K13, GPIO.OUT)       #schaltetvS1 Steuerleitung Förderband, siehe Bedienungsanleitung
#GPIO.setup(K14, GPIO.OUT)       #schaltet S2 Steuerleitung Förderband, siehe Bedienungsanleitung

#Initialisierung der Output GPIOs --> Aktoren in Grundstellung bringen

#GPIO.output(K9, GPIO.HIGH)   # 1Y1 = HIGH ->  Grundstellung Zylinder A1
#GPIO.output(K10, GPIO.LOW)   # 1Y2 = LOW  ->  Grundstellung Zylinder A1
#GPIO.output(K11, GPIO.LOW)   # 2Y1 = LOW  ->  Grundstellung Zylinder A2
#GPIO.output(K12, GPIO.LOW)   # 3Y1 = LOW  ->  Grundstellung Zylinder A3
#GPIO.output(K13, GPIO.LOW)   # Anschluss S1,  Beschaltung siehe Bedienungsanleitung
#GPIO.output(K14, GPIO.LOW)   # Anschluss S2,  Beschaltung siehe Bedienungsanleitung


def Komponenten_test():
    print("Achtung, in 5 Sekunden beginnt der Test aller Komponenten")
    time.sleep(5)

    GPIO.output(K14, GPIO.HIGH)     # Strom auf Steuerleitung S2 des Förderbands und
    GPIO.output(K13, GPIO.LOW)      # Stromlos Steuerleiung S1 des Förderband. Somit läuft das Förderband im Linkslauf -> Siehe Bedienungsanleitung

    print("Förderband Linkslauf")



    time.sleep(5)
    print("Bitte die Lichtschranken am geünschten Zylinder abdecken, um diesen auszufahren. Achtung Verletzungsgefahr")
    while True:
        time.sleep(0.1)
        if GPIO.input(K1) == GPIO.HIGH :                    # Wenn Lichtschranke 1 einen Gegenstand detektiert, dann
            print("Gegenstand in Lichtschranke 1 erkannt")
            GPIO.output(K9, GPIO.LOW)                       # wird 1Y1 stromlos gemacht
            GPIO.output(K10, GPIO.HIGH)                     # und 1Y2 mit Strom versorgt, so dass der Zylinder 1A ausfahren kann


        if GPIO.input(K4) == GPIO.HIGH :                    # Wenn der Endlagensensor 1S2 des Zylinders 1A ein Singnal ausgibt, dann
            GPIO.output(K9, GPIO.HIGH)                      # wird 1Y1 mit strom versorgt
            GPIO.output(K10, GPIO.LOW)                      # und 1Y2 mit stromlos gemacht, so dass der Zylinder 1A einfahren kann


        if GPIO.input(K2) == GPIO.HIGH :
            print("Gegenstand in Lichtschranke 2 erkannt")
            GPIO.output(K11, GPIO.HIGH)


        if GPIO.input(K5) == GPIO.HIGH :
            GPIO.output(K11, GPIO.LOW)


        if GPIO.input(K3) == GPIO.HIGH :
            print("Gegenstand in Lichtschranke 3 erkannt")
            GPIO.output(K12, GPIO.HIGH)


        if GPIO.input(K6) == GPIO.HIGH :
            GPIO.output(K12, GPIO.LOW)


        if GPIO.input(K3) == GPIO.HIGH and  GPIO.input(K2) == GPIO.HIGH:
            GPIO.output(K14, GPIO.LOW)
            GPIO.output(K13, GPIO.LOW)
            print("Förderband aus")

        if GPIO.input(K2) == GPIO.HIGH and GPIO.input(K1) == GPIO.HIGH:
            GPIO.output(K14, GPIO.HIGH)
            GPIO.output(K13, GPIO.LOW)
            print("Rechtslauf ein")

def collect_data():
    num = 1

    GPIO.output(K14, GPIO.HIGH)     # Strom auf Steuerleitung S2 des Förderbands und
    GPIO.output(K13, GPIO.LOW)      # Stromlos Steuerleiung S1 des Förderband. Somit läuft das Förderband im Linkslauf -> Siehe Bedienungsanleitung

    cap = cv2.VideoCapture(0)

    while True:
        ret, img = cap.read()
        cv2.imshow('Frame', img)
        if GPIO.input(K3) == GPIO.HIGH:

            time.sleep(0)

            print("Lichtschranke ausgelöst")
            GPIO.output(K13, GPIO.LOW)
            GPIO.output(K14, GPIO.LOW)

            i=0
            while i<10:
                time.sleep(1)
                ret, img = cap.read()
                i=i+1
            i=0
            cv2.imshow('Frame', img)
            cv2.imwrite('/home/pi/images/'+str(num)+'.jpg', img)
            print('Bild ' +str(num)+ ' aufgenommen')

            time.sleep(2)

            num = num +1

            GPIO.output(K14, GPIO.HIGH)     # Strom auf Steuerleitung S2 des Förderbands und
            GPIO.output(K13, GPIO.LOW)      # Stromlos Steuerleiung S1 des Förderband. Somit läuft das Förderband im Linkslauf -> Siehe Bedienungsanleitung

        if cv2.waitKey(1) & 0xFF == ord('y'):
            GPIO.output(K13, GPIO.LOW)
            GPIO.output(K14, GPIO.LOW)
            break

#pass

#collect_data()

#cv2.destroyAllWindows()
#Komponenten_test()

test = Machine()

while True:
    print(test.get_ls_1())
