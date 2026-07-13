#!/usr/bin/env python3
"""
Motor a pasos (stepper) con driver A4988 / DRV8825 - Una sola dirección
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

PASOS_POR_VUELTA = 200      # 1.8° por paso, sin microstepping
RETARDO_SEG = 0.001         # 1000 microsegundos -> controla la velocidad

DIRECCION = True            # True = horario, False = antihorario (fija)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    GPIO.setup(EN_PIN, GPIO.OUT)

    GPIO.output(EN_PIN, GPIO.LOW)          # habilitar el driver
    GPIO.output(DIR_PIN, GPIO.HIGH if DIRECCION else GPIO.LOW)  # dirección fija

    print("Iniciando motor stepper (una sola dirección)...")

def mover_motor(pasos):
    for _ in range(pasos):
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(RETARDO_SEG)
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(RETARDO_SEG)

def main():
    setup()
    try:
        while True:
            print("Girando (1 vuelta)...")
            mover_motor(PASOS_POR_VUELTA)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Programa detenido por el usuario")
    finally:
        GPIO.output(EN_PIN, GPIO.HIGH)  # deshabilitar driver
        GPIO.cleanup()

if __name__ == "__main__":
    main()