# Anlegen der Klasse Maschine
# Über die Methoden der Klasse Maschine lassen sich sämtliche Anlagenkomponenten steuern
import time
import cv2
import RPi.GPIO as GPIO
import datetime
import serial

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
        self.K7 = 26  #Endlagensensor Zylinder 3 -> 3S2
        #Die jeweiligen Pins als Input zuweisen, außerdem softwaremaessige Verwendung der internern Pull-Down Widerstaende

        GPIO.setup(self.K1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.K7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

    # Methoden zur Ansteuerung der Anlagenkomponenten

    def get_ls_1(self):                     #falls Lichtschranke1 ausgelöst wird, wird True und ein Text zurückgegeben
        if GPIO.input(self.K1) == GPIO.HIGH :
            print("LS1 ein")
            return True
        else:
            return False
        pass

    def get_ls_2(self):                     #falls Lichtschranke2 ausgelöst wird, wird True und ein Text zurückgegeben
        if GPIO.input(self.K2) == GPIO.HIGH :
            print("LS2 ein")
            return True
        else:
            return False
        pass

    def get_ls_3(self):                     #falls Lichtschranke3 ausgelöst wird, wird True und ein Text zurückgegeben
        if GPIO.input(self.K3) == GPIO.HIGH :
            print("LS3 ein")
            return True
        else:
            return False
        pass

    def get_ls_4(self):                     #falls Lichtschranke4 ausgelöst wird, wird True und ein Text zurückgegeben
        if GPIO.input(self.K7) == GPIO.HIGH :
            print("LS4 ein")
            return True
        else:
            return False
        pass

    def get_zyl_1(self):                    # Abfrage der Endlage des 1 Zylinders
        if GPIO.input(self.K4) == GPIO.HIGH :
            print("Zyl1 Endlage")
            return True
        else:
            return False
        pass

    def get_zyl_2(self):                    # Abfrage der Endlage des 2 Zylinders
        if GPIO.input(self.K5) == GPIO.HIGH :
            print("Zyl2 Endlage")
            return True
        else:
            return False
        pass

    def get_zyl_3(self):                    # Abfrage der Endlage des 3 Zylinders

        if GPIO.input(self.K6) == GPIO.HIGH :
            print("Zyl3 Endlage")
            return True
        else:
            return False
        pass

    def start_belt_rl(self):                #Das Fließband startet mit Rechtslauf

        GPIO.output(self.K14, GPIO.HIGH)
        GPIO.output(self.K13, GPIO.LOW)
        print("Rechtslauf ein")
        pass

    def start_belt_ll(self):                #Das Fließband startet mit Linkslauf

        GPIO.output(self.K13, GPIO.HIGH)
        GPIO.output(self.K14, GPIO.LOW)
        print("Linkslauf ein")
        pass

    def stop_belt(self):                    #Das Fließband stoppt

        GPIO.output(self.K14, GPIO.LOW)
        GPIO.output(self.K13, GPIO.LOW)
        print("Förderband aus")
        pass

    def start_ver(self):                    #Start des Motors für die Vereinzelung
        usb_ard = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(1)
        usb_ard.flush()
        usb_ard.write(b"start\n")


    def stop_ver(self):                     #Stopp des Motors für die Vereinzelung
        usb_ard = serial.Serial('/dev/ttyUSB0', 9600)
        time.sleep(1)
        usb_ard.flush()
        usb_ard.write(b"stop\n")

    def push_zyl_1(self):                   #Ausfahren des 1 Zylinders

        GPIO.output(self.K9, GPIO.LOW)
        GPIO.output(self.K10, GPIO.HIGH)
        print("Zylinder 1 ausfahren")
        pass

    def push_zyl_2(self):                   #Ausfahren des 2 Zylinders

        GPIO.output(self.K11, GPIO.HIGH)
        print("Zylinder 2 ausfahren")
        pass

    def push_zyl_3(self):                   #Ausfahren des 3 Zylinders

        GPIO.output(self.K12, GPIO.HIGH)
        print("Zylinder 3 ausfahren")
        pass

    def pull_zyl_1(self):                   #Einfahren des 1 Zylinders

        GPIO.output(self.K9, GPIO.HIGH)
        GPIO.output(self.K10, GPIO.LOW)
        print("Zylinder 1 einfahren")
        pass

    def pull_zyl_2(self):                   #Einfahren des 2 Zylinders

        GPIO.output(self.K11, GPIO.LOW)
        print("Zylinder 2 einfahren")
        pass

    def pull_zyl_3(self):                   #Einfahren des 3 Zylinders

        GPIO.output(self.K12, GPIO.LOW)
        print("Zylinder 3 einfahren")
        pass


    def ea_test(self):                      #Test aller Komponenten außer des Vereinzelungsmotors
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

        pass

    def collect_data(self):                 #Automatische Erstellung der Bilder (Band hält an, Bild wird gemacht)
        num = 1

        self.start_belt_rl

        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            cv2.imshow('Frame', img)
            if self.get_ls_3:

                print("Lichtschranke ausgelöst")
                self.stop_belt

                cv2.imshow('Frame', img)
                cv2.imwrite('/home/pi/images/'+datetime.datetime.now().replace(microsecond=0).isoformat()+'.jpg', img)
                print('Bild ' +str(num)+ ' aufgenommen')

                num = num +1

                self.start_belt_rl

            if cv2.waitKey(1) & 0xFF == ord('y'):
                self.stop_belt
                break

    pass

    def picture(self, index):                 #Automatische Erstellung der Bilder (Bild wird gemacht ohne das Band zu stoppen)


        cap = cv2.VideoCapture(0)

        while True:
            ret, img = cap.read()
            print('Bild ' +str(index)+ ' aufgenommen')
            return img

    pass




    def take_pictures(self):                # händische Erstellung der Bilder mit der Y Taste
        num=0
        cap = cv2.VideoCapture(0)
        while True:
            ret, img = cap.read()
            cv2.imshow('Frame', img)
            if cv2.waitKey(1) & 0xFF == ord('y'):
                cv2.imwrite('/home/pi/images/kunststoff/ch/'+datetime.datetime.now().replace(microsecond=0).isoformat()+'.jpg', img)
                print('Bild ' +str(num)+ ' aufgenommen')
                num=num+1

            if cv2.waitKey(1) & 0xFF == ord('e'):
                break
    pass

    def delay(self,duration_in_seconds):    # Einbringung einer Verzögerung, verwendet als Alternative zur sleep-methode
        current_time = datetime.datetime.now()
        end_time = current_time + datetime.timedelta(0,duration_in_seconds)
        while current_time<end_time:
            current_time = datetime.datetime.now()
    pass

    def param_ver(self):                    # Methode zur Anpassung der Vereinzelungs-Parameter über das Hauptmenü
        while True:
            eingabe=input("Bitte geben Sie ihren Befehl ein, x zum verlassen!")
            if eingabe == "x":
                return
            else:
                usb_ard = serial.Serial('/dev/ttyUSB0', 9600)
                time.sleep(1)
                usb_ard.flush()
                usb_ard.write(eingabe.encode())
    pass