# -*- coding: utf-8 -*-

import time                     #Para las pausas
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)        #Usar la numeración de pines de la placa

pinDir = 24                     #Pin DIR
pinStep = 26                    #Pin Step
numSteps = 200                  #Número de pasos del motor
microPausa = 0.005              #Número de segundos de pausa


GPIO.setup(pinDir,GPIO.OUT)
GPIO.setup(pinStep,GPIO.OUT)

while True:

        GPIO.output(pinDir,0)           #Establezco una dirección (0 o 1)

        for x in range(0,numSteps):
                GPIO.output(pinStep, True)
                time.sleep(microPausa)
                GPIO.output(pinStep, False)
                time.sleep(microPausa)

        time.sleep(microPausa)

        GPIO.output(pinDir, 1)          #Cambio de dirección

        for x in range(0,numSteps):
                GPIO.output(pinStep, True)
                time.sleep(microPausa)
                GPIO.output(pinStep, False)
                time.sleep(microPausa)

GPIO.cleanup()          #Para acabar correctamente