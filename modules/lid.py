# Anlegen der verschiedenen Deckelarten (inklusive Ausschuss) durch Vererbung von der Klasse "Lid"
# Zuordnung einer Soll-Position (Behälternummer 1-3, Ausschuss: Nummer 4) zu jeder Deckel-Klasse
import time
import cv2
import datetime
import serial

class Lid():  #Klasse zum Erstellen von Deckeln
    

    def __init__(self, soll):
        self.__position_soll = soll #Speicherung der Soll-Position der jeweiligen Deckelklasse
        pass

    def get_pos_soll(self):  #Methode zur Rückgabe der Soll-Position
        return self.__position_soll
        pass


class Kronkorken(Lid): #Klasse zum Erstellen von Kronkorken, erbt von Klasse Lid
    
    def __init__(self,soll = 1):
        super().__init__(soll)       


    
class Metall(Lid): #Klasse zum Erstellen von Metalldeckeln, erbt von Klasse Lid

    def __init__(self, soll = 2):
        super().__init__(soll)
    

class Kunststoff(Lid): #Klasse zum Erstellen von Kunststoffdeckeln, erbt von Klasse Lid

    def __init__(self, soll = 3):
        super().__init__(soll)

class Ausschuss(Lid): #Klasse zum Erstellen vo Ausschuss, erbt von Klasse Lid

    def __init__(self, soll = 4): #Ausschuss wird in keinen der drei Behälter geschoben und fällt am Ende des Fließbands in das Ausschuss-Behältnis
        super().__init__(soll)