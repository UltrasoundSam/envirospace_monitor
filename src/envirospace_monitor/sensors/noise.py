'''Noise sensor implementation using microphone hardware.

Provides a NoiseSensor class that reads sound amplitude from a microphone
using the enviroplus noise module.
'''

import datetime as dt

import numpy as np
import numpy.typing as npt
import sounddevice as sd

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
    def __init__(self,
                 sample_rate: int = 16_000,
                 duration: float = 2.0,
                 freq_range: tuple[int, int] = (FREQ_LOW, FREQ_HIGH)):
        super().__init__(SensorType.NOISE)
        self.duration = duration
        self.sample_rate = sample_rate
        self.freq_range = freq_range

        # Create audio stream object
        self._stream = sd.InputStream(
            device='adau7002',
            samplerate=self.sample_rate,
            channels=1,
            dtype='float32'
        )

        # Start stream and sleep for 2 seconds to get rid of transient
        self._stream.start()
        sd.sleep(2000)

    def close(self) -> None:
        '''Closes off Stream when destroy class'''
        self._stream.stop()
        self._stream.close()

    def read(self) -> SensorReading:
        """Read the mean amplitude of frequencies in the configured range."""
        # Validate frequency range
        if self.freq_range[0] > self.freq_range[1]:
            raise ValueError("Frequency range low must be less than or equal to high")

        # Checks that request is fully Nyquisted
        nyquist = self.sample_rate // 2
        if self.freq_range[0] > nyquist or self.freq_range[1] > nyquist:
            raise ValueError(f"Frequency range exceeds Nyquist frequency {nyquist:,} Hz")

        # Record data from microphone
        data = self._record()

        # Remove any initial values and then the DC offset
        data = data[1000:]
        data -= np.mean(data)

        # Calculates FFT
        npow2 = int(np.ceil(np.log2(len(data))))
        magnitude = np.abs(np.fft.rfft(data, n=2**npow2))
        freqs = np.fft.rfftfreq(2**npow2, 1 / self.sample_rate)

        # Create filter to get frequencies of interest
        mask = (freqs >= self.freq_range[0]) & (freqs <= self.freq_range[1])
        magnitude_filtered = magnitude[mask]

        # Records mean amplitude of frequencies in the range
        mean_volume = np.mean(magnitude_filtered)
        return SensorReading(
            timestamp=dt.datetime.now(dt.UTC),
            sensor_type=self.sensor_type,
            value=mean_volume
        )

    def _record(self) -> npt.NDArray[np.float32]:
        '''Records audio from sound device for analysis'''

        # Calculate how many samples to read and get them
        samples = int(self.duration * self.sample_rate)
        data, _overflowed = self._stream.read(samples)

        # if overflowed:
        #     print("Audio overflow detected")

        return np.squeeze(data)
