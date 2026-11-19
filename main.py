'''Orchestrator for the data pipeline.'''

# Initially, I want to just be able to capture values
import sys
import time

from bme280 import BME280

from envirospace_monitor.sensors import (
    HumiditySensor,
    LightSensor,
    PressureSensor,
    TemperatureSensor,
    NoiseSensor,
)

DELAY = 5   # Delay between readings in seconds

# Import BME280 sensor from board
bme280 = BME280()

# Import sensor objects
noise_sensor = NoiseSensor()
light_sensor = LightSensor()
temperature_sensor = TemperatureSensor(bme280)
pressure_sensor = PressureSensor(bme280)
humidity_sensor = HumiditySensor(bme280)

sensor_collection = (
    noise_sensor,
    light_sensor,
    temperature_sensor,
    pressure_sensor,
    humidity_sensor
)

try:
    while True:
        readings = [sensor.read() for sensor in sensor_collection]
        for reading in readings:
            print(reading)
        time.sleep(DELAY)

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)
