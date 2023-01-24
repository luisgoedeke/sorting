#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Import von notwendigen Biblitheken
import sys
import time
import cv2                     #Bibliothek zum ansprechen der Kamera (Opencv)
import RPi.GPIO as GPIO        #Biblitheke, um die GPIO Pine per Programm ansprechen/auslesen zu können.
import serial
from tkinter import *
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

root = Tk()

button_func = Button(root, text="Funktionstest", width=40, height=2, font=120, bg="purple", command=m.ea_test)
button_take_pictures = Button(root, text="Bilder aufnehmen", width=40, height=2, font=120, bg="purple", command=m.take_pictures)
button_ver_start = Button(root, text="Vereinzelung starten", width=40, height=2, font=120, bg="green", command=m.ver_start)
button_ver_stop = Button(root, text="Vereinzelung stoppen", width=40, height=2, font=120, bg="red", command=m.ver_stop)
button_para_ver = Button(root, text="Vereinzelung Parameter", width=40, height=2, font=120, bg="yellow", command=m.param_ver)
button_belt_start = Button(root, text="Band starten", width=40, height=2, font=120, bg="green", command=m.start_belt_rl)
button_belt_stop = Button(root, text="Band stoppen", width=40, height=2, font=120, bg="red", command=m.stop_belt)
button_sort_start = Button(root, text="Sortierung starten", width=40, height=2, font=120, bg="green", command=sorting.sort)

button_func.pack()
button_take_pictures.pack()
button_ver_start.pack()
button_ver_stop.pack()
button_para_ver.pack()
button_belt_start.pack()
button_belt_stop.pack()
button_sort_start.pack()


root.mainloop()

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
        

