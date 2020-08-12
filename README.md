# IoT_Datenanalyse_in_Gebauden
This project build a IoT network to monitor 4 room of an office.


IoT Datenanalyse in Gebauden from

Bachelor Thesis of Enea Gentilini at the FHNW Muttenz, 2020

This packages run a IoT network to monitor 4 rooms and collect data on an external server. 

Necessary equipment for this project:
1x RsPi 4
4x RsPi Zero W con accessori
5x SD Card
4x Pimoroni Enviro +
4x Seed Studio Grove CO2 & Temp & Humidity Sensor 
4x Pimoroni Particulate Matter Sensor with Cable
2x Kamera with Fish Eye Objektiv
2x Seed Grove VOC and eCO2
2x Seed Grove PIR Motion Sensor
1x Seed Grove Universal 4Pin 5cm Cable 5pc
1x Seed Grove Universal 4Pin 20cm Cable 5pc
1x Seed Grove Universal 4Pin 30cm Cable 5pc
1x Wireless Router
1x external server (InfluxDB and Grafana could also be installed on the Raspberry Pi 4)

Description of the scripts:

Set_up_zero:
Run this to install all the necessary modules on each RsPi Zero
#Before running the set up script do the following steps for each Raspberry Pi Zero:
# 1) Format SD Card
# 2) Install Raspbian
# 3) Go to Raspberry Pi Configuration --> Interfaces --> Enable camera
# 4) Run this script

Zero_settings_BUX.py
This settings script set specific values for each Basic Unit. In this file you have to enable all the connected sensors

Enviro_script.py
This script read measurements from the Enviro module (You don’t have to run it)

sgp30_script.py
This script read measurements from the SGP30 module (You don’t have to run it)

zero_to_mqtt.py
This module read measurements from the modules (Enviro, SGP30, SCD30) and send it to the Broker via MQTT (RUN IT on your Raspberry Pi zero, Basic Unit)

pir_to_mqtt.py
This scripts detect movements from the PIR motion sensors and send the number of people detected on the image to the broke via MQTT.

#MQTTInfluxDBBrifge.py
This script need to be run on the RaspberryPi Zero, before you have to install and sett Mosquito (MQTT) on your Raspberry Pi 4 and set it as broker
You also have to insert your MQTT credential and Server informations in this script
