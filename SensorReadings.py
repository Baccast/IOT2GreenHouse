#!/usr/bin/env python
import time
import ADC0832
import RPi.GPIO as GPIO
import math

# Constants for the thermistor characteristics
R0 = 10000  # Resistance at a known temperature (in ohms)
T0 = 25     # Known temperature in Celsius (adjust as needed)
B = 3950    # Beta coefficient of the thermistor (adjust as needed)

# GPIO pin for photoresistor
PHOTORESISTOR_PIN = 0

# GPIO pin for thermistor
THERMISTOR_PIN = 1

def temperature_from_resistance(Rt):
    try:
        # Calculate temperature in Celsius using the Steinhart-Hart equation
        inv_T = 1.0 / (T0 + 273.15) + (1.0 / B) * math.log(Rt / R0)
        temperature_C = 1.0 / inv_T - 273.15
        return temperature_C
    except ValueError:
        # Handle the case where math.log() receives an invalid argument
        return None

def read_photoresistor():
    try:
        # Read photoresistor value from ADC channel 0
        photoresistor_value = ADC0832.getADC(PHOTORESISTOR_PIN)
        return photoresistor_value
    except KeyboardInterrupt:
        GPIO.cleanup()

def read_thermistor():
    try:
        # Read thermistor value from ADC channel 1
        thermistor_value = ADC0832.getADC(THERMISTOR_PIN)
        return thermistor_value
    except KeyboardInterrupt:
        GPIO.cleanup()

def main():
    try:
        ADC0832.setup()

        while True:
            try:
                # Read and print photoresistor value
                photoresistor_value = read_photoresistor()
                light_or_dark = None
                # Convert photoresistor value to either light or dark
                if photoresistor_value > 100:
                    light_or_dark = "light"
                else:
                    light_or_dark = "dark"
                print(f"Light Status: {light_or_dark}")

                # Read and print thermistor value
                thermistor_value = read_thermistor()
                # Convert thermistor value to temperature in degrees Celsius
                Rt_temp = 3.3 * float(thermistor_value) / 255
                temperature_C = temperature_from_resistance(Rt_temp)
                print(f"Temperature: {temperature_C} degrees Celsius")
            
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
