#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from adc0832 import ADC0832  

# GPIO Pins
MOISTURE_SENSOR_PIN = 26
PHOTORESISTOR_CHANNEL = 0

# Sensor Thresholds
TEMPERATURE_THRESHOLD = 25.0  # Adjust as needed
SOIL_MOISTURE_THRESHOLD = 500  # Adjust as needed

# ADC Configuration
adc = ADC0832()

def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(MOISTURE_SENSOR_PIN, GPIO.IN)

def destroy():
    GPIO.cleanup()

def is_daytime():
    # You may need to adjust this logic based on the actual behavior of your light sensor
    # For example, if a lower ADC value indicates more light, you may need to modify the comparison.
    light_value = adc.getResult(PHOTORESISTOR_CHANNEL)
    return light_value > LIGHT_THRESHOLD

def read_moisture():
    # You may need to adjust this logic based on the behavior of your moisture sensor
    return GPIO.input(MOISTURE_SENSOR_PIN)

def read_temperature_humidity():
    # Assuming DHT11 sensor, change to Adafruit_DHT.DHT22 for DHT22
    sensor = Adafruit_DHT.DHT11
    pin = 17  # GPIO pin where the DHT11 sensor is connected

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    return humidity, temperature

if __name__ == '__main__':
    setup()
    try:
        while True:
            humidity, temperature = read_temperature_humidity()
            moisture = read_moisture()

            print(f'Temperature: {temperature}°C, Humidity: {humidity}%, Moisture: {moisture}')

            if is_daytime():
                print('It is daytime.')

                # Your logic for daytime conditions here
                if temperature > TEMPERATURE_THRESHOLD:
                    print('Temperature is too high. Activate fan for 30 seconds.')
                    # Code to activate fan for 30 seconds goes here

                if moisture < SOIL_MOISTURE_THRESHOLD:
                    print('Soil moisture is too low. Activate water pump for 3 seconds.')
                    # Code to activate water pump for 3 seconds goes here

            else:
                print('It is nighttime.')

                # Your logic for nighttime conditions here
                # For example, turn on grow lamp if it is dark
                # Code to control grow lamp goes here

            time.sleep(1)  # Adjust the sleep duration as needed

    except KeyboardInterrupt:
        destroy()
