#!/usr/bin/env python
import time
import ADC0832
import RPi.GPIO as GPIO

# GPIO pin for photoresistor
PHOTORESISTOR_PIN = 0

# GPIO pin for thermistor
THERMISTOR_PIN = 1

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
            # Read and print photoresistor value
            photoresistor_value = read_photoresistor()
            print(f"Photoresistor Value: {photoresistor_value}")

            # Read and print thermistor value
            thermistor_value = read_thermistor()
            print(f"Thermistor Value: {thermistor_value}")

            time.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
