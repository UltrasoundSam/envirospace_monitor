'''Sensor classes for the envirospace monitor.

This package provides a hierarchy of sensor classes, including:
- Abstract base class (Sensor)
- Sensor reading dataclass (SensorReading)
- Sensor type enum (SensorType)
- Concrete sensor implementations (LightSensor, TemperatureSensor, etc.)
'''

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType
from envirospace_monitor.sensors.humidity import HumiditySensor
from envirospace_monitor.sensors.light import LightSensor
from envirospace_monitor.sensors.noise import NoiseSensor
from envirospace_monitor.sensors.pressure import PressureSensor
from envirospace_monitor.sensors.temperature import TemperatureSensor

__all__ = [
    "Sensor",
    "SensorReading",
    "SensorType",
    "HumiditySensor",
    "LightSensor",
    "NoiseSensor",
    "PressureSensor",
    "TemperatureSensor"
]
