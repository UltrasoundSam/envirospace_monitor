'''Creates a base class for all sensors to inherit from,
as well as a dataclass to hold sensor readings and status.
'''

import datetime as dt
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class SensorType(Enum):
    """Enum for sensor types."""
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    LIGHT = "light"
    NOISE = "noise"


@dataclass
class SensorReading:
    """Dataclass to hold sensor readings."""
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
        """Convert the SensorReading to a dictionary."""
        return {
            "sensor_type": self.sensor_type.value,
            "value": self.value,
            "unit": self.unit,
            "timestamp": self.timestamp.isoformat()
        }


class Sensor(ABC):
    """Abstract base class for all sensors."""

    def __init__(self, sensor_type: SensorType):
        self._sensor_type = sensor_type

    @property
    def sensor_type(self) -> SensorType:
        """The type of sensor this is."""
        return self._sensor_type

    @abstractmethod
    def read(self) -> SensorReading:
        """Read the sensor and return a SensorReading."""
