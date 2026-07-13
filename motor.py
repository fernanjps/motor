"""
Prueba de motor a pasos (stepper) con driver A4988
Raspberry Pi 3B+ - Python 3 + RPi.GPIO

Conexiones sugeridas (BCM):
    DIR  -> GPIO 20
    STEP -> GPIO 21
    EN   -> GPIO 16  (opcional, LOW = driver habilitado)

Recuerda alimentar el A4988 (VMOT/GND) con una fuente externa
adecuada al motor, NUNCA con el 5V del Raspberry Pi.
"""

import RPi.GPIO as GPIO
import time

# --- Configuración de pines ---
DIR = 20
STEP = 21
EN = 16

# --- Configuración del motor ---
PASOS_POR_VUELTA = 200   # Motor típico de 1.8° por paso (sin microstepping)
VELOCIDAD = 0.001        # segundos entre pulsos (menor = más rápido)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Habilitar el driver (en A4988, EN en LOW = habilitado)
GPIO.output(EN, GPIO.LOW)


def mover_motor(pasos, direccion, velocidad=VELOCIDAD):
    """
    Mueve el motor un número de pasos en una dirección.
    direccion: 1 = horario, 0 = antihorario
    """
    GPIO.output(DIR, direccion)
    for _ in range(pasos):
        GPIO.output(STEP, GPIO.HIGH)
        time.sleep(velocidad)
        GPIO.output(STEP, GPIO.LOW)
        time.sleep(velocidad)


def main():
    try:
        while True:
            print("Girando sentido horario (1 vuelta)...")
            mover_motor(PASOS_POR_VUELTA, 1)
            time.sleep(1)

            print("Girando sentido antihorario (1 vuelta)...")
            mover_motor(PASOS_POR_VUELTA, 0)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nPrueba detenida por el usuario.")

    finally:
        GPIO.output(EN, GPIO.HIGH)  # deshabilitar driver
        GPIO.cleanup()
        print("GPIO liberados. Programa finalizado.")


if __name__ == "__main__":
    main()