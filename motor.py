#!/usr/bin/env python3
"""
Motor a pasos (stepper) con driver A4988 / DRV8825
Giro continuo en sentido horario
Raspberry Pi 3B+ (usando RPi.GPIO)

Conexiones (numeración BCM):
    DIR  -> GPIO27 (pin físico 13)
    STEP -> GPIO17 (pin físico 11)
    EN   -> GPIO22 (pin físico 15)   (opcional, LOW = driver habilitado)
"""

import RPi.GPIO as GPIO
import time

# Pines BCM
DIR_PIN = 27
STEP_PIN = 17
EN_PIN = 22

RETARDO_SEG = 0.005   # controla la velocidad (menor = más rápido)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(EN_PIN, GPIO.OUT)

    GPIO.output(EN_PIN, GPIO.LOW)     # habilitar el driver
    GPIO.output(DIR_PIN, GPIO.HIGH)   # sentido horario (fijo)

    print("Girando en sentido horario de forma continua... (Ctrl+C para detener)")

def main():
    setup()
    try:
        while True:
            GPIO.output(STEP_PIN, GPIO.HIGH)
            time.sleep(RETARDO_SEG)
            GPIO.output(STEP_PIN, GPIO.LOW)
            time.sleep(RETARDO_SEG)
    except KeyboardInterrupt:
        print("\nMotor detenido por el usuario")
    finally:
        GPIO.output(EN_PIN, GPIO.HIGH)  # deshabilitar driver
        GPIO.cleanup()

if __name__ == "__main__":
    main()