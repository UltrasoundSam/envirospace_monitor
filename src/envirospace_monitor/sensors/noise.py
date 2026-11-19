'''Noise sensor implementation using microphone hardware.

Provides a NoiseSensor class that reads sound amplitude from a microphone
using the enviroplus noise module.
'''

import datetime as dt
from enviroplus.noise import Noise

from envirospace_monitor.sensors.base import Sensor, SensorReading, SensorType

# Default frequency range for noise measurement
FREQ_LOW = 400
FREQ_HIGH = 3_000


class NoiseSensor(Sensor):
    """Sensor for reading noise level from a microphone.

    Args:
        noise_obj: An initialized Noise sensor instance.
        freq_range: Tuple of (low, high) frequencies in Hz to measure.
            Defaults to (400, 3000) Hz.
    """
    def __init__(self, noise_obj: Noise,
                 freq_range: tuple[float, float] = (FREQ_LOW, FREQ_HIGH)):
        super().__init__(SensorType.NOISE)
        self._sensor = noise_obj
        self.freq_range = freq_range

    def read(self) -> SensorReading:
        """Read the mean amplitude of frequencies in the configured range."""
        # Records mean amplitude of frequencies in the range
        mean_volume = self._sensor.get_amplitude_at_frequency_range(*self.freq_range)
        return SensorReading(
            timestamp=dt.datetime.now(dt.timezone.utc),
            sensor_type=self.sensor_type,
            value=mean_volume
        )
