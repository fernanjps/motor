#!/usr/bin/env python3
# =======================================
# Raspberry Pi 3B+ + L298N
# Prueba de motor DC - movimiento por pasos/pulsos
# Cada pulso tiene su propia duración independiente
# =======================================
import RPi.GPIO as GPIO
import time

# -------- Pines del L298N (numeración BCM) --------
IN1 = 13
IN2 = 19
ENA = 26

# -------- Configuración --------
velocidad = 40        # 0-100 (baja esto para que vaya más lento; prueba 30-50)
pwmFreq = 1000         # Frecuencia del PWM en Hz

# -------- Duración de cada pulso (en segundos) --------
# Cada elemento de la lista es un pulso independiente.
# Ejemplo: parte 1 = 4s, parte 2 = 5s, parte 3 = 2s, parte 4 = 3s
duracionesPulsos = [4, 5, 2, 3]

pausaEntrePulsos = 0.3  # segundos de pausa entre pulsos
tiempoPausa = 1         # pausa entre cambio de sentido

# -------- Setup GPIO --------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, pwmFreq)
pwm.start(0)

def detener_motor():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

def girar_adelante():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(velocidad)

def girar_atras():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(velocidad)

def mover_por_partes(funcion_direccion, nombre):
    total_partes = len(duracionesPulsos)
    for i, duracion in enumerate(duracionesPulsos):
        print(f"{nombre} - parte {i+1}/{total_partes} ({duracion}s)")
        funcion_direccion()
        time.sleep(duracion)
        detener_motor()
        time.sleep(pausaEntrePulsos)

try:
    detener_motor()
    print("Prueba de motor DC iniciada (movimiento por partes)...")
    while True:
        mover_por_partes(girar_atras, "ATRAS")
        print("Pausa entre cambio de sentido...")
        detener_motor()
        time.sleep(tiempoPausa)

        mover_por_partes(girar_adelante, "ADELANTE")
        print("Pausa entre cambio de sentido...")
        detener_motor()
        time.sleep(tiempoPausa)

except KeyboardInterrupt:
    print("\nPrograma interrumpido por el usuario.")
finally:
    detener_motor()
    pwm.stop()
    GPIO.cleanup()
    print("GPIO liberado correctamente.")