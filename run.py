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
from stepper_param import *
from datetime import date

def stepper_param():
    param = Toplevel(root)
    param.title = "Parameter Schrittmotor"
    param.geometry("600x400")

    steps_rl_label = Label(param, text = "Schritte Rechtslauf").place(x = 10,y = 40)
    steps_ll_label = Label(param, text = "Schritte Linkslauf").place(x = 10, y = 80)
    delay_label = Label(param, text = "Verzögerung [ms]").place(x = 10, y = 120)
    times_full_rot_label = Label(param, text = "Anzahl volle Umdrehungen").place(x = 10, y = 160)
    steps_rl = Entry(param).place(x = 200, y = 40)
    steps_ll = Entry(param).place(x = 200, y = 80)
    delay = Entry(param).place(x = 200, y = 120)
    times_full_rot = Entry(param).place(x = 200, y = 160)
    steps_rl_button = Button(param, text= "Übernehmen").place(x = 400, y = 35)
    steps_ll_button = Button(param, text= "Übernehmen").place(x = 400, y = 75)
    delay_button = Button(param, text= "Übernehmen").place(x = 400, y = 115)
    times_full_rot_button = Button(param, text= "Übernehmen").place(x = 400, y = 155)

m = Machine()
sorting = Sorting(m)

root = Tk()

root.title("Sortieranlage")

button_func = Button(root, text="Funktionstest", width=40, height=2, font=120, bg="purple", command=m.ea_test)
button_take_pictures = Button(root, text="Bilder aufnehmen", width=40, height=2, font=120, bg="purple", command=m.take_pictures)
button_ver_start = Button(root, text="Vereinzelung starten", width=40, height=2, font=120, bg="green", command=m.start_ver)
button_ver_stop = Button(root, text="Vereinzelung stoppen", width=40, height=2, font=120, bg="red", command=m.stop_ver)
button_para_ver = Button(root, text="Vereinzelung Parameter", width=40, height=2, font=120, bg="yellow", command=stepper_param)
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

        

