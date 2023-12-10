#!/usr/bin/env python
import ADC0832
import time
import threading
import RPi.GPIO as GPIO

# Constants for the thermistor characteristics
R0 = 10000  # Resistance at a known temperature (in ohms)
T0 = 25     # Known temperature in Celsius (adjust as needed)
B = 3950    # Beta coefficient of the thermistor (adjust as needed)

# GPIO pins for the LEDs
LED1_PIN = 23
LED2_PIN = 24

def init():
    ADC0832.setup()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED1_PIN, GPIO.OUT)  # Set up LED1 pin as an output
    GPIO.setup(LED2_PIN, GPIO.OUT)  # Set up LED2 pin as an output
    GPIO.output(LED1_PIN, GPIO.LOW)  # Turn off LED1 initially
    GPIO.output(LED2_PIN, GPIO.LOW)  # Turn off LED2 initially

def map_value(value, from_min, from_max, to_min, to_max):
    # Map 'value' from the range [from_min, from_max] to [to_min, to_max]
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

def temperature_from_resistance(Rt):
    try:
        # Calculate temperature in Celsius using the Steinhart-Hart equation
        inv_T = 1.0 / (T0 + 273.15) + (1.0 / B) * (Rt / R0)
        temperature_C = 1.0 / inv_T - 273.15
        return temperature_C
    except ValueError:
        # Handle the case where math.log() receives an invalid argument
        return None

def update_temperature():
    while True:
        # Read photoresistor and thermistor values from ADC channels
        res_light = ADC0832.getADC(0)  # Photoresistor connected to channel 0
        res_temp = ADC0832.getADC(1)   # Thermistor connected to channel 1

        # Check the light level and update the labels
        if res_light < 128:
            # Turn on both LEDs when it's dark
            GPIO.output(LED1_PIN, GPIO.HIGH)
            GPIO.output(LED2_PIN, GPIO.HIGH)
        else:
            # Turn off both LEDs when it's light
            GPIO.output(LED1_PIN, GPIO.LOW)
            GPIO.output(LED2_PIN, GPIO.LOW)

        # Calculate temperature in Celsius
        Vr_temp = 3.3 * float(res_temp) / 255
        Rt_temp = 10000 * Vr_temp / (3.3 - Vr_temp)
        temperature_C = temperature_from_resistance(Rt_temp)

        if temperature_C is not None:
            temperature_F = (temperature_C * 9/5) + 32  # Convert to Fahrenheit

            print(f'Light Status: {"Dark" if res_light < 128 else "Light"}')
            print(f'Temperature (Celsius): {temperature_C:.2f}°C')
            print(f'Temperature (Fahrenheit): {temperature_F:.2f}°F')

        time.sleep(0.2)

def cleanup():
    # Turn off both LEDs
    GPIO.output(LED1_PIN, GPIO.LOW)
    GPIO.output(LED2_PIN, GPIO.LOW)
    # Clean up GPIO
    GPIO.cleanup()

def main():
    init()

    # Start the temperature update thread
    update_thread = threading.Thread(target=update_temperature)
    update_thread.daemon = True
    update_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        cleanup()

if __name__ == '__main__':
    main()
