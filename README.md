Greenhouse Monitoring System
Overview
This project is a Greenhouse Monitoring System implemented on a Raspberry Pi. It integrates various sensors to monitor temperature, humidity, soil moisture, and light intensity. The system also controls actuators such as a water pump and a fan to maintain optimal greenhouse conditions.

Components
Raspberry Pi
Sensor and Actuator Connections
DHT-11 Temperature and Humidity Sensor: GPIO 26
Photoresistor: ADC Channel 0
Soil Moisture Sensor: ADC Channel 1
DC Fan: A=GPIO 6, B=GPIO 13
Relay Module: GPIO 4
LED 1: GPIO 23
LED 2: GPIO 24
ADC0832 Setup
ADC_CS: 11
ADC_CLK: 13
ADC_DIO: 12
Setup Instructions
Hardware Connections:

Connect DHT-11 to GPIO pin 26 for temperature and humidity sensing.
Connect the Photoresistor to ADC channel 0 for light intensity.
Connect the Soil Moisture sensor to ADC channel 1 if available.
Connect the DC Fan for ventilation with A to GPIO 6 and B to GPIO 13.
Connect the Relay Module to GPIO 4 to control the water pump.
Connect LED 1 to GPIO 23 and LED 2 to GPIO 24 for additional indicators.
Setup ADC0832 with the provided pins (ADC_CS, ADC_CLK, ADC_DIO).
Software Setup:

Clone the repository to your Raspberry Pi.
Install necessary Python libraries using pip install -r requirements.txt.
Make sure you have the necessary credentials for ThingsBoard MQTT (host, port, and token).
Run the System:

Execute the main script using python greenhouse_monitor.py.
The system will continuously monitor the environment and publish data to ThingsBoard.
Additional Notes
Adjust threshold values in the script based on your greenhouse requirements.
Uncomment the read_soil_moisture function if you have a soil moisture sensor connected to ADC0832.
