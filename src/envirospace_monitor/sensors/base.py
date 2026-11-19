'''Base classes and types for the sensor system.

This module contains the foundational types and abstract base classes that
all concrete sensor implementations build upon.
'''

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class SensorType(Enum):
    """Supported sensor types and their corresponding units.

    Attributes:
        TEMPERATURE: Temperature readings, unit: °C
        HUMIDITY: Relative humidity, unit: %
        PRESSURE: Atmospheric pressure, unit: hPa
        LIGHT: Light intensity, unit: Lux
        NOISE: Sound level, unit: dB
    """
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    LIGHT = "light"
    NOISE = "noise"


@dataclass
class SensorReading:
    """A single reading from a sensor.

    Attributes:
        timestamp: When the reading was taken (timezone-aware UTC recommended).
        sensor_type: The type of sensor that produced this reading.
        value: The numeric value of the reading.
        unit: The unit of measurement (auto-filled from sensor_type if None).
    """
    timestamp: dt.datetime
    sensor_type: SensorType
    value: float
    unit: str | None = None

    _UNIT_MAP: ClassVar[dict[SensorType, str]] = {
        SensorType.TEMPERATURE: "°C",
        SensorType.HUMIDITY: "%",
        SensorType.PRESSURE: "hPa",
        SensorType.LIGHT: "Lux",
        SensorType.NOISE: "dB"
    }

    def __post_init__(self):
        """Auto-fill unit based on sensor_type if not provided."""
        if self.unit is None:
            self.unit = self._UNIT_MAP.get(self.sensor_type, "unknown")

    def __str__(self) -> str:
        return f"{self.timestamp.isoformat()} - {self.sensor_type.value.capitalize()}: {self.value} {self.unit}"

    def to_dict(self) -> dict:
        """Convert the reading to a JSON-serializable dictionary."""
        return {
            "sensor_type": self.sensor_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat()
        }


class Sensor(ABC):
    """Abstract base class for all physical sensors.

    Subclasses must implement:
        - sensor_type property: The type of sensor this is
        - read() method: Returns a SensorReading
    """

    def __init__(self, sensor_type: SensorType):
        self._sensor_type = sensor_type

    @property
    def sensor_type(self) -> SensorType:
        """The type of sensor this is."""
        return self._sensor_type

    @abstractmethod
    def read(self) -> SensorReading:
        """Take a reading from the sensor and return it."""
