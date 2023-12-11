#!/usr/bin/env python
import RPi.GPIO as GPIO
import Adafruit_DHT
import ADC0832
import time
import paho.mqtt.client as mqtt

# Motor Pins
FAN_PIN_A = 6
FAN_PIN_B = 13
RELAY_PIN = 4  # GPIO for the Relay Module
DHT_PIN = 26

# Global Variables
fan_cooldown = False

# ThingsBoard MQTT settings
TB_HOST = "mqtt.thingsboard.cloud"
TB_PORT = 1883
TB_TOKEN = "TUczvTkZxb5KZGoOnpKH"
TB_TOPIC = "v1/devices/me/telemetry"

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")

def setup_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.username_pw_set(username=TB_TOKEN)
    client.connect(TB_HOST, TB_PORT, 60)
    return client

def publish_to_thingsboard(client, data):
    client.publish(TB_TOPIC, data)

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)  # Suppress GPIO warnings
    GPIO.setup(FAN_PIN_A, GPIO.OUT)
    GPIO.setup(FAN_PIN_B, GPIO.OUT)
    GPIO.setup(RELAY_PIN, GPIO.OUT)  # Relay Module control pin
    GPIO.output(FAN_PIN_A, GPIO.HIGH)
    GPIO.output(FAN_PIN_B, GPIO.HIGH)
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the water pump initially
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
        time.sleep(30)
        control_fan(0)
        fan_cooldown = False

def read_temperature_and_humidity_sensor():
    sensor = Adafruit_DHT.DHT11
    humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)

    if humidity is not None and temperature is not None:
        print(f'Temperature (DHT-11): {temperature:.2f}°C, Humidity: {humidity:.2f}%')
        return temperature, humidity
    else:
        print('Failed to read data from DHT-11 sensor')
        return None, None

""" def read_soil_moisture():
    res = ADC0832.getADC()
    moisture = 255 - res
    print(f'Soil Moisture: {moisture}')
    return moisture """

def read_light_status():
    light_value = ADC0832.getADC(0)  # Read from ADC0832 channel 0
    print(f'Light Status: {"Day" if light_value < 100 else "Night"}')
    return "Day" if light_value < 100 else "Night"

def control_water_pump(status=0):
    if status == 1:
        GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn on the water pump
        print("Water Pump is On")
    else:
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn off the water pump
        print("Water Pump is Off")

def main_loop():
    mqtt_client = setup_mqtt()

    while True:
        temperature_C, humidity = read_temperature_and_humidity_sensor()
        soil_moisture = read_soil_moisture()
        light_status = read_light_status()

        # Adjust this condition for fan control based on temperature
        if temperature_C is not None and temperature_C > 30:
            run_fan_with_cooldown()

        # Adjust this condition for water pump control based on any criteria you like
        # For now, it simply checks if the temperature is above 30
        if temperature_C is not None and temperature_C > 30:
            control_water_pump(1)  # Turn on the water pump
        else:
            control_water_pump(0)  # Turn off the water pump

        # Publish temperature, humidity, soil moisture, and light status to ThingsBoard
        if temperature_C is not None and humidity is not None:
            payload = f'{{"temperature":{temperature_C},"humidity":{humidity},"soil_moisture":{soil_moisture},"light_status":"{light_status}"}}'
            publish_to_thingsboard(mqtt_client, payload)

        time.sleep(2)

def cleanup():
    GPIO.cleanup()

if __name__ == '__main__':
    setup()
    try:
        main_loop()
    except KeyboardInterrupt:
        cleanup()
