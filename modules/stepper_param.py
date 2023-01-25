import sys
import time
from machine import *
from tkinter import *

def stepper_param(m):
    param = Tk()
    param.title = "Parameter Schrittmotor"
    param.geometry("300x400")

    steps_rl_label = Label(param, text = "Schritte Rechtslauf").place(x = 10,y = 40)
    steps_ll_label = Label(param, text = "Schritte Linkslauf").place(x = 10, y = 80)
    delay_label = Label(param, text = "Verzögerung [ms]").place(x = 10, y = 120)
    delay_label = Label(param, text = "Anzahl volle Umdrehungen").place(x = 10, y = 160)
    steps_rl = Entry(param).place(x = 200, y = 40)
    steps_ll = Entry(param).place(x = 200, y = 80)
    delay = Entry(param).place(x = 200, y = 120)
    times_full_rot = Entry(param).place(x = 200, y = 160)

    param.mainloop()
