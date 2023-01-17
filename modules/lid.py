import time
import cv2
import datetime
import serial

class Lid():  #Klasse zum Erstellen von Deckeln

    def __init__(self, position_now):
        self.position_now = position_now #Variable zur Speicherung der aktuellen Position




class Kronkorken(Lid): #Klasse zum erstellen von Kronkorken, erbt von Klasse Lid

    def __init__(self, position_now):
        super().__init__(position_now) #Initalisieren über Eltern-Klasse (Lid)


    
class Metall(Lid): #Klasse zum erstellen von Metalldeckeln, erbt von Klasse Lid

    def __init__(self, position_now):
        super().__init__(position_now) #Initalisieren über Eltern-Klasse (Lid)



class Kunststoff(Lid): #Klasse zum erstellen von Kunststoffdeckeln, erbt von Klasse Lid

    def __init__(self, position_now):
        super().__init__(position_now) #Initalisieren über Eltern-Klasse (Lid)
