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
from datetime import date
test = Machine()
sorting = Sorting()

#Schleife zum ständigen wiederholen des Hauptmenues

while True:

    auswahl = input("Willkommen im Hauptmenue! \n Bitte waehlen sie eine Option: \n 1: Starten der Vereinzelung \n 2: Stoppen der Vereinzelung \n 3: Funktionstest der Maschine starten \n 4: Bilder aufnehmen \n 5: Sortierung starten \n")

    if auswahl == "1":
        test.start_ver()

    if auswahl == "2":
        test.stop_ver()

    if auswahl == "3":
        test.ea_test()

    if auswahl == "4":
        test.take_pictures()
        
    if auswahl == "5":
        sorting.sort()    

    else:
        print("Sie haben keine gueltige Eingabe getroffen.")
