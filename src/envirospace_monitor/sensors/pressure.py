'''Pressure sensor implementation using BME280 hardware.

Provides a PressureSensor class that reads atmospheric pressure from a BME280
sensor device.
'''

import datetime as dt
from bme280 import BME280

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType


class PressureSensor(Sensor):
    """Sensor for reading atmospheric pressure from a BME280 device.

    Args:
        sensor_obj: An initialized BME280 sensor instance.
    """
    def __init__(self, sensor_obj: BME280):
        super().__init__(SensorType.PRESSURE)
        self._sensor = sensor_obj

    def read(self) -> SensorReading:
        """Read the current atmospheric pressure in hPa."""
        return SensorReading(
            timestamp=dt.datetime.now(dt.timezone.utc),
            sensor_type=self.sensor_type,
            value=self._sensor.get_pressure()
        )
