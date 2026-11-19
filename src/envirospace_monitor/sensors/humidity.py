import datetime as dt

from bme280 import BME280

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType


class HumiditySensor(Sensor):
    def __init__(self, sensor_obj: BME280):
        self._sensor = sensor_obj

    @property
    def sensor_type(self) -> SensorType:
        return SensorType.HUMIDITY

    def read(self) -> SensorReading:
        return SensorReading(
            timestamp=dt.datetime.now(dt.UTC),
            sensor_type=self.sensor_type,
            value=self._sensor.get_humidity()
        )
