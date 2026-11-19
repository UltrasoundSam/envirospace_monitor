'''Light sensor implementation using LTR559 hardware.

Provides a LightSensor class that reads light intensity (lux) from an LTR559
sensor device.
'''

import datetime as dt
from ltr559 import LTR559

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType


class LightSensor(Sensor):
    """Sensor for reading light intensity from an LTR559 device.

    Note:
        The first reading from LTR559 is often inaccurate, so it is discarded
        during initialization.
    """

    def __init__(self):
        super().__init__(SensorType.LIGHT)
        self._ltr559 = LTR559()

        # First reading always appears off, so discard it
        _ = self._ltr559.get_lux()

    def read(self) -> SensorReading:
        """Read the current light intensity in lux."""
        lux = self._ltr559.get_lux()
        return SensorReading(
            timestamp=dt.datetime.now(dt.timezone.utc),
            sensor_type=self.sensor_type,
            value=lux
        )
