#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Import von notwendigen Biblitheken
import sys
import time
import cv2                     #Bibliothek zum ansprechen der Kamera (Opencv)
import RPi.GPIO as GPIO        #Biblitheke, um die GPIO Pine per Programm ansprechen/auslesen zu können.
import serial
sys.path.insert(0, './modules')
from machine import *
from sorting import *
from lid import *
from datetime import date
from threading import Thread
m = Machine()
sorting = Sorting(m)

#Schleife zum ständigen wiederholen des Hauptmenues

#deckel1 = Kunststoff()
#deckel2 = Metall()
#deckel3 = Kronkorken()
#print(deckel1.get_pos_soll())
#print(deckel2.get_pos_soll())
#print(deckel3.get_pos_soll())

while True:

    auswahl = input("Willkommen im Hauptmenue! \n Bitte waehlen sie eine Option: \n 1: Starten der Vereinzelung \n 2: Stoppen der Vereinzelung \n 3: Funktionstest der Maschine starten \n 4: Bilder aufnehmen \n 5: Sortierung starten \n 6: Parameter der Vereinzelung anpassen \n 7: Band starten \n 8: Band stoppen \n")

    if auswahl == "1":
        m.start_ver()

    elif auswahl == "2":
        m.stop_ver()

    elif auswahl == "3":
        m.ea_test()

    elif auswahl == "4":
        m.take_pictures()
        
    elif auswahl == "5":
        sorting.sort()

    elif auswahl == "6":
        m.param_ver()
    
    elif auswahl == "7":
        m.start_belt_rl()
        
    elif auswahl == "8":
        m.stop_belt()

    else:
        print("Sie haben keine gueltige Eingabe getroffen.")
        

