# Programm zum Testen der Bilderkennung (bzw. des TFLite models)
# Einlesen der bearbeiteten Bilder und des TFLite models 
# Ausgabe der Klassifizierung (Angabe jeweils in %)
import os
import numpy as np
import tflite_runtime.interpreter as tflite
import cv2
import pathlib

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="/home/pi/images/bilder bearbeitet/model.tflite")

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

interpreter.allocate_tensors()

# input details
print(input_details)
# output details
print(output_details)

    
for file in pathlib.Path("/home/pi/images/bilder bearbeitet/kronkorken/cc").iterdir():
    
    # read and resize the image
    img = cv2.imread(r"{}".format(file.resolve()))
    new_img = cv2.resize(img, (224, 224))
    
    # input_details[0]['index'] = the index which accepts the input
    interpreter.set_tensor(input_details[0]['index'], [new_img])
    
    # run the inference
    interpreter.invoke()
    
    # output_details[0]['index'] = the index which provides the input
    output_data = interpreter.get_tensor(output_details[0]['index']) 
    
    # Ausgabe der Klassifizierung (Angabe jeweils in % umgerechnet)
    print(output_data[0][0]/255*100,"% Kronkorken", output_data[0][1]/255*100,"% Metall", output_data[0][2]/255*100, "% Kunststoff")
