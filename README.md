# IOT2GreenHouse
Greenhouse Monitoring System
Overview
This project is a Greenhouse Monitoring System implemented on a Raspberry Pi. It integrates various sensors to monitor temperature, humidity, soil moisture, and light intensity. The system also controls actuators such as a water pump and a fan to maintain optimal greenhouse conditions.

Components
Raspberry Pi
DHT-11 Temperature and Humidity Sensor
ADC0832 Analog-to-Digital Converter for Light Intensity
Relay Module for Water Pump
DC Fan for Ventilation
Setup Instructions
Hardware Connections:

Connect DHT-11 to GPIO pin 26 for temperature and humidity sensing.
Connect ADC0832 to read light intensity from channel 0.
Connect the Relay Module to control the water pump.
Connect the DC Fan for ventilation.
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
