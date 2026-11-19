'''Humidity sensor implementation using BME280 hardware.

Provides a HumiditySensor class that reads relative humidity from a BME280
sensor device.
'''

import datetime as dt

from bme280 import BME280

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType


class HumiditySensor(Sensor):
    """Sensor for reading relative humidity from a BME280 device.

    Args:
        sensor_obj: An initialized BME280 sensor instance.
    """
    def __init__(self, sensor_obj: BME280):
        super().__init__(SensorType.HUMIDITY)
        self._sensor = sensor_obj

    def read(self) -> SensorReading:
        """Read the current relative humidity percentage."""
        return SensorReading(
            timestamp=dt.datetime.now(dt.UTC),
            sensor_type=self.sensor_type,
            value=self._sensor.get_humidity()
        )
