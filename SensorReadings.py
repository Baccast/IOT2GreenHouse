#!/usr/bin/env python
import os
import RPi.GPIO as GPIO
import ADC0832
import Adafruit_DHT
import time
import math

# Motor Pins
FAN_PIN_A = 6
FAN_PIN_B = 13
MOISTURE_SENSOR_PIN = 26  # GPIO for the DHT-11 sensor

# Global Variables
fan_cooldown = False

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN_A, GPIO.OUT)
    GPIO.setup(FAN_PIN_B, GPIO.OUT)
    GPIO.output(FAN_PIN_A, GPIO.HIGH)
    GPIO.output(FAN_PIN_B, GPIO.HIGH)
    stop_fan()
    ADC0832.setup()

def stop_fan():
    GPIO.output(FAN_PIN_A, GPIO.HIGH)
    GPIO.output(FAN_PIN_B, GPIO.HIGH)

def control_fan(status=0, direction=1):
    if status == 0:
        stop_fan()
        print("Fan is Off")
    else:
        if direction == 1:
            print("Fan is On")
            GPIO.output(FAN_PIN_A, GPIO.HIGH)
            GPIO.output(FAN_PIN_B, GPIO.LOW)
        else:
            GPIO.output(FAN_PIN_A, GPIO.LOW)
            GPIO.output(FAN_PIN_B, GPIO.HIGH)

def run_fan_with_cooldown():
    global fan_cooldown

    if not fan_cooldown:
        fan_cooldown = True
        control_fan(1)
        time.sleep(15)
        control_fan(0)
        fan_cooldown = False

def read_temperature_sensor():
    T25 = 25 + 273.15
    R25 = 10000
    B = 3455

    res = ADC0832.getADC(0)
    Vr = 3.3 * float(res) / 255

    try:
        Rt = (3.3 * 10000) / Vr - 10000
        if Rt == 0:
            Rt = 0.1
    except ZeroDivisionError:
        Rt = 0.1

    ln = math.log(Rt / R25)
    Tk = 1 / ((ln / B) + (1 / T25))
    Tc = Tk - 273.15

    Tc = round(Tc, 2)
    return Tc

def read_moisture_sensor():
    # Use the Adafruit_DHT library to read data from the DHT-11 sensor
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, MOISTURE_SENSOR_PIN)

    if humidity is not None and temperature is not None:
        print(f'Moisture: {humidity}%')
        print(f'Temperature (DHT-11): {temperature:.2f}°C')
    else:
        print('Failed to read data from DHT-11 sensor')

def main_loop():
    while True:
        temperature_C = read_temperature_sensor()
        print(f'Temperature (Celsius): {temperature_C:.2f}°C')

        read_moisture_sensor()

        # Adjust this condition for fan control
        if temperature_C > 30:
            run_fan_with_cooldown()

        time.sleep(2)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main_loop()
    except KeyboardInterrupt:
        cleanup()
        ADC0832.destroy()
