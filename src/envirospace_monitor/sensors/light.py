'''Has code for Light sensor class'''

import datetime as dt

from ltr559 import LTR559

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType


class LightSensor(Sensor):
    """Class for the light sensor."""

    def __init__(self):
        super().__init__(SensorType.LIGHT)
        self._ltr559 = LTR559()

        # First reading always appears off, so discard it
        _ = self._ltr559.get_lux()

    def read(self) -> SensorReading:
        """Read the light sensor and return a SensorReading."""
        lux = self._ltr559.get_lux()
        return SensorReading(
            timestamp=dt.datetime.now(dt.UTC),
            sensor_type=self.sensor_type,
            value=lux
        )
