# import useful module and setting of the Basic Unit
import zero_settings

###   Enviro+   ###
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

from bme280 import BME280

# sets up the variables for the sensor
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

#Definition of the functions to read measurements
def enviro_get_temperature():
    temperature = bme280.get_temperature() + zero_settings.temp_compensation
    temperature = round((temperature), 2)
    temperature = str(temperature)
    return (temperature)

def enviro_get_pressure():
    pressure = bme280.get_pressure()
    pressure = round((pressure), 2)
    pressure = str(pressure)
    return (pressure)

def enviro_get_humidity():
    humidity = bme280.get_humidity()
    humidity = round((humidity), 2)
    humidity = str(humidity)
    return (humidity)

# Particulate Matter detection
from pms5003 import PMS5003

pms5003 = PMS5003()
pm_readings = pms5003.read()

def enviro_get_pm1():
    value = pm_readings.pm_ug_per_m3(1)
    value = round((value), 2)
    value = str(value)
    return (value)

def enviro_get_pm2_5():
    value = pm_readings.pm_ug_per_m3(2.5)
    value = round((value), 2)
    value = str(value)
    return (value)

def enviro_get_pm10():
    value = pm_readings.pm_ug_per_m3(10)
    value = round((value), 2)
    value = str(value)
    return (value)

# Light detection
from ltr559 import LTR559

ltr559 = LTR559()

def enviro_get_luminosity():
    luminosity = ltr559.get_lux()
    luminosity = round((luminosity), 2)
    luminosity = str(luminosity)
    return (luminosity)

def enviro_get_proximity():
    proximity = ltr559.get_proximity()
    proximity = round((proximity), 2)
    proximity = str(proximity)
    return (proximity)

# Gas detection
from enviroplus import gas

readings = gas.read_all()

def enviro_get_reducing():
    reducing = readings.reducing
    reducing = round((reducing), 2)
    reducing = str(reducing)
    return (reducing)

def enviro_get_oxidising():
    oxidising = readings.oxidising
    oxidising = round((oxidising), 2)
    oxidising = str(oxidising)
    return (oxidising)

def enviro_get_nh3():
    nh3 = readings.nh3
    nh3 = round((nh3), 2)
    nh3 = str(nh3)
    return (nh3)
