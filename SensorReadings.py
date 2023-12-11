#!/usr/bin/env python
import RPi.GPIO as GPIO
import Adafruit_DHT
import ADC0832
import time

# Motor Pins
FAN_PIN_A = 6
FAN_PIN_B = 13
MOISTURE_SENSOR_PIN = 1  # GPIO for the Soil Moisture Detector
RELAY_PIN = 4  # GPIO for the Relay Module

# Global Variables
fan_cooldown = False

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN_A, GPIO.OUT)
    GPIO.setup(FAN_PIN_B, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT)  # Relay Module control pin
    GPIO.output(FAN_PIN_A, GPIO.HIGH)
    GPIO.output(FAN_PIN_B, GPIO.HIGH)
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the water pump initially
    stop_fan()

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
        time.sleep(30)
        control_fan(0)
        fan_cooldown = False

def read_temperature_sensor():
    sensor = Adafruit_DHT.DHT11
    _, temperature = Adafruit_DHT.read_retry(sensor, MOISTURE_SENSOR_PIN)

    if temperature is not None:
        print(f'Temperature (DHT-11): {temperature:.2f}°C')
        return temperature
    else:
        print('Failed to read data from DHT-11 sensor')
        return None

def read_soil_moisture_sensor():
    moisture_value = ADC0832.getResult(MOISTURE_SENSOR_PIN)
    print(f'Soil Moisture: {moisture_value}')
    return moisture_value

def control_water_pump(status=0):
    if status == 1:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn on the water pump
        print("Water Pump is On")
    else:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the water pump
        print("Water Pump is Off")

def main_loop():
    while True:
        temperature_C = read_temperature_sensor()
        moisture_value = read_soil_moisture_sensor()

        # Adjust this condition for fan control based on temperature or moisture
        if temperature_C is not None and temperature_C > 30:
            run_fan_with_cooldown()

        # Adjust this condition for water pump control based on soil moisture
        if moisture_value is not None and moisture_value < 100:  # Adjust the threshold as needed
            control_water_pump(1)  # Turn on the water pump
        else:
            control_water_pump(0)  # Turn off the water pump

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
