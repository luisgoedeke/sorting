#! /usr/bin/env python
# -*- coding: utf-8 -*-


# Import von notwendigen Biblitheken
import sys
import time
import cv2
import RPi.GPIO as GPIO        #Biblitheke, um die GPIO Pine per Programm ansprechen/auslesen zu können.
import serial
sys.path.insert(0, './modules')
from machine import *
from datetime import date

#collect_data()

test = Machine()

test.start_ver()

time.sleep(15)

test.stop_ver()

#test.ea_test()
