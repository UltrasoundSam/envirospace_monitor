'''Orchestrator for the data pipeline.'''

# Initially, I want to just be able to capture values
import json
import os
import sys
import time

import paho.mqtt.client as mqtt
from bme280 import BME280
from dotenv import load_dotenv

from envirospace_monitor.sensors import (
    HumiditySensor,
    LightSensor,
    NoiseSensor,
    PressureSensor,
    TemperatureSensor,
)

DELAY = 60   # Delay between readings in seconds

# Load environment variables from .env file
load_dotenv()

# MQTT Configuration (from environment variables)
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_BASE_TOPIC = os.getenv("MQTT_BASE_TOPIC")
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

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

# MQTT Client setup
mqtt_client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    protocol=mqtt.MQTTv311
)
mqtt_client.tls_set()  # Enable TLS for secure connection
if MQTT_USERNAME and MQTT_PASSWORD:
    mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)

try:
    mqtt_client.loop_start()
    while True:
        readings = [sensor.read() for sensor in sensor_collection]
        for reading in readings:
            # Publish to MQTT
            topic = f"{MQTT_BASE_TOPIC}/{reading.sensor_type.value}"
            payload = json.dumps(reading.to_dict())
            mqtt_client.publish(topic, payload)
            # Also print to console for local visibility
            print(f"Published to {topic}: {payload}")
        time.sleep(DELAY)

except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    sys.exit(0)
