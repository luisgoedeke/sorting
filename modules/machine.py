import time
import RPi.GPIO as GPIO

class Machine:
    def __init__(self):
        #########################################################################################################
        #Grundeinstellungen für die GPIOs

        GPIO.setmode(GPIO.BOARD)  #legt fest, wie die GPIO Pine im nachfolgenden Programm benannt werden müssen
        GPIO.setwarnings(False)   # Warnungen werden unterdrückt
        #########################################################################################################

        # Inputs
        # GPIO Pins werden entsprechende Variablen zuweisen

        self.K1 = 23   #Lichtschranke 1 -> 1S1E
        self.K2 = 24   #Lichtschranke 2 -> 2S1E
        self.K3 = 7    #Lichtschranke 3 -> 3S1E
        self.K4 = 8    #Endlagensensor Zylinder 1 -> 1S2
        self.K5 = 10   #Endlagensensor Zylinder 2 -> 2S2
        self.K6 = 11   #Endlagensensor Zylinder 3 -> 3S2
        #Die jeweiligen Pins als Input zuweisen, außerdem softwaremaessige Verwendung der internern Pull-Down Widerstaende

        GPIO.setup(self.K1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # Outputs
        # GPIO Pins werden entsprechende Variablen zuweisen

        self.K9 =  12    #Relais  K9 wird über den GPIO12 angsteuert.
        self.K10 = 13    #Relais K10 wird über den GPIO13 angsteuert.
        self.K11 = 15    #Relais k11 wird über den GPIO15 angsteuert.
        self.K12 = 16    #Relais K12 wird über den GPIO16 angsteuert.
        self.K13 = 18    #Relais K13 wird über den GPIO18 angsteuert.
        self.K14 = 19    #Relais K14 wird über den GPIO19 angsteuert.

        #Die jeweiligen Pins als Output festlegen

        GPIO.setup(self.K9,  GPIO.OUT)       #schaltet 5/2 Wegventil -> 1Y1
        GPIO.setup(self.K10, GPIO.OUT)       #chaltet 5/2 Wegventil -> 1Y2
        GPIO.setup(self.K11, GPIO.OUT)       #schaltet 5/2 Wegeventil mit Federrückstellung -> 2Y1
        GPIO.setup(self.K12, GPIO.OUT)       #schaltet 5/2 Wegeventil mit Federrückstellung -> 3Y1
        GPIO.setup(self.K13, GPIO.OUT)       #schaltetvS1 Steuerleitung Förderband, siehe Bedienungsanleitung
        GPIO.setup(self.K14, GPIO.OUT)       #schaltet S2 Steuerleitung Förderband, siehe Bedienungsanleitung

        #Initialisierung der Output GPIOs --> Aktoren in Grundstellung bringen

        GPIO.output(self.K9, GPIO.HIGH)   # 1Y1 = HIGH ->  Grundstellung Zylinder A1
        GPIO.output(self.K10, GPIO.LOW)   # 1Y2 = LOW  ->  Grundstellung Zylinder A1
        GPIO.output(self.K11, GPIO.LOW)   # 2Y1 = LOW  ->  Grundstellung Zylinder A2
        GPIO.output(self.K12, GPIO.LOW)   # 3Y1 = LOW  ->  Grundstellung Zylinder A3
        GPIO.output(self.K13, GPIO.LOW)   # Anschluss S1,  Beschaltung siehe Bedienungsanleitung
        GPIO.output(self.K14, GPIO.LOW)   # Anschluss S2,  Beschaltung siehe Bedienungsanleitung
        pass

    def get_ls_1(self):
        time.sleep(1)
        if GPIO.input(self.K1) == GPIO.HIGH :
            print("LS1 ein")
            return True
        else:
            return False
        pass

    def get_ls_2(self):
        if GPIO.input(self.K2) == GPIO.HIGH :
            print("LS2 ein")
            return True
        else:
            return False
        pass

    def get_ls_3(self):
        if GPIO.input(self.K3) == GPIO.HIGH :
            print("LS3 ein")
            return True
        else:
            return False
        pass

    def get_zyl_1(self):
        if GPIO.input(self.K4) == GPIO.HIGH :
            print("Zyl1 Endlage")
            return True
        else:
            return False
        pass

    def get_zyl_2(self):
        if GPIO.input(self.K5) == GPIO.HIGH :
            print("Zyl2 Endlage")
            return True
        else:
            return False
        pass

    def get_zyl_3(self):

        if GPIO.input(self.K6) == GPIO.HIGH :
            print("Zyl3 Endlage")
            return True
        else:
            return False
        pass

    def start_belt_rl(self):

        GPIO.output(self.K14, GPIO.HIGH)
        GPIO.output(self.K13, GPIO.LOW)
        print("Rechtslauf ein")
        pass

    def start_belt_ll(self):

        GPIO.output(self.K13, GPIO.HIGH)
        GPIO.output(self.K14, GPIO.LOW)
        print("Linkslauf ein")
        pass

    def stop_belt(self):

        GPIO.output(self.K14, GPIO.LOW)
        GPIO.output(self.K13, GPIO.LOW)
        print("Förderband aus")
        pass

    def push_zyl_1(self):

        GPIO.output(self.K9, GPIO.LOW)
        GPIO.output(self.K10, GPIO.HIGH)
        print("Zylinder 1 ausfahren")
        pass

    def push_zyl_2(self):

        GPIO.output(self.K11, GPIO.HIGH)
        print("Zylinder 2 ausfahren")
        pass

    def push_zyl_3(self):

        GPIO.output(self.K12, GPIO.HIGH)
        print("Zylinder 3 ausfahren")
        pass

    def pull_zyl_1(self):
        
        GPIO.output(self.K9, GPIO.HIGH)
        GPIO.output(self.K10, GPIO.LOW)
        print("Zylinder 1 einfahren")
        pass
    
    def pull_zyl_2(self):

        GPIO.output(self.K11, GPIO.LOW)
        print("Zylinder 2 einfahren")
        pass
    
    def pull_zyl_3(self):

        GPIO.output(self.K12, GPIO.LOW)
        print("Zylinder 3 einfahren")
        pass
    
    def ea_test(self):
        while not self.get_ls_1():
            time.sleep(1)
    
        while not self.get_ls_2():
            time.sleep(1)

        while not self.get_ls_3():
            time.sleep(1)
    
        self.start_belt_rl()

        time.sleep(10)

        self.stop_belt()

        self.start_belt_ll()

        time.sleep(10)

        self.push_zyl_1()
    
        while not self.get_zyl_1():
            time.sleep(1)
    
        self.pull_zyl_1()

        self.push_zyl_2()
    
        while not self.get_zyl_2():
            time.sleep(1)
    
        self.pull_zyl_2()

        self.push_zyl_3()
    
        while not self.get_zyl_3():
            time.sleep(1)
    
        self.pull_zyl_3()

        self.stop_belt()
        