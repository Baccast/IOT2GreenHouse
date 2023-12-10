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
                temperature = (thermistor_value - 500) / 10
                print(f"Temperature: {temperature} degrees Celsius")
            
                time.sleep(1)
            except Exception as e:
                print(f"Unexpected error: {e}")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
