#!/usr/bin/env python3
# =======================================
# Raspberry Pi 3B+ + L298N
# Prueba de motor DC - movimiento por pasos/pulsos
# Gira ADELANTE en pulsos, se detiene,
# gira ATRAS en pulsos, y repite
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

# -------- Tiempos para movimiento "por partes" --------
duracionPulso = 0.5    # segundos que gira en cada pulso
pausaEntrePulsos = 0.3 # segundos de pausa entre pulsos
numPulsos = 15         # cuántos pulsos hace en cada sentido
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
    for i in range(numPulsos):
        print(f"{nombre} - pulso {i+1}/{numPulsos}")
        funcion_direccion()
        time.sleep(duracionPulso)
        detener_motor()
        time.sleep(pausaEntrePulsos)

try:
    detener_motor()
    print("Prueba de motor DC iniciada (movimiento por partes)...")
    while True:
        mover_por_partes(girar_adelante, "ADELANTE")
        print("Pausa entre cambio de sentido...")
        detener_motor()
        time.sleep(tiempoPausa)

        mover_por_partes(girar_atras, "ATRAS")
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