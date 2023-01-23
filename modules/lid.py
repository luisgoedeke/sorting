import time
import cv2
import datetime
import serial

class Lid():  #Klasse zum Erstellen von Deckeln
    

    def __init__(self, soll):
        self.__position_soll = soll
        pass

    def get_pos_soll(self):
        return self.__position_soll
        pass


class Kronkorken(Lid): #Klasse zum erstellen von Kronkorken, erbt von Klasse Lid
    
    def __init__(self,soll = 1):
        super().__init__(soll)       


    
class Metall(Lid): #Klasse zum erstellen von Metalldeckeln, erbt von Klasse Lid

    def __init__(self, soll = 2):
        super().__init__(soll)
    

class Kunststoff(Lid): #Klasse zum erstellen von Kunststoffdeckeln, erbt von Klasse Lid

    def __init__(self, soll = 3):
        super().__init__(soll)

class Ausschuss(Lid): #Klasse zum erstellen vom Ausschuss, erbt von Klasse Lid

    def __init__(self, soll = 4):
        super().__init__(soll)