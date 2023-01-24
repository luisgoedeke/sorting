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

root = Tk()

root.title("Sortieranlage")

button_func = Button(root, text="Funktionstest", width=40, height=2, font=120, bg="purple", command=m.ea_test)
button_take_pictures = Button(root, text="Bilder aufnehmen", width=40, height=2, font=120, bg="purple", command=m.take_pictures)
button_ver_start = Button(root, text="Vereinzelung starten", width=40, height=2, font=120, bg="green", command=m.start_ver)
button_ver_stop = Button(root, text="Vereinzelung stoppen", width=40, height=2, font=120, bg="red", command=m.stop_ver)
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

        

