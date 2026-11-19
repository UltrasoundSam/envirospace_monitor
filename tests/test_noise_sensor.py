"""Unit tests for the NoiseSensor class.

These tests mock the sounddevice module to test the NoiseSensor
without requiring actual microphone hardware.
"""

import datetime as dt
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from envirospace_monitor.sensors.base import SensorReading, SensorType
from envirospace_monitor.sensors.noise import FREQ_HIGH, FREQ_LOW, NoiseSensor

# Test constants
DEFAULT_SAMPLE_RATE = 16_000
DEFAULT_DURATION = 2.0
DEFAULT_FREQ_RANGE = (FREQ_LOW, FREQ_HIGH)


@pytest.fixture
def mock_sounddevice():
    """Fixture to mock the sounddevice module."""
    with patch('envirospace_monitor.sensors.noise.sd') as mock_sd:
        # Setup mock stream
        mock_stream = MagicMock()
        mock_sd.InputStream.return_value = mock_stream
        mock_sd.sleep = MagicMock()
        yield mock_sd, mock_stream


@pytest.fixture
def noise_sensor(mock_sounddevice):
    """Fixture to create a NoiseSensor with mocked sounddevice."""
    sensor = NoiseSensor(
        sample_rate=DEFAULT_SAMPLE_RATE,
        duration=DEFAULT_DURATION,
        freq_range=DEFAULT_FREQ_RANGE
    )
    yield sensor
    # Cleanup - ensure stream is closed
    sensor.close()


class TestNoiseSensorInit:
    """Tests for NoiseSensor initialization."""

    def test_init_defaults(self, mock_sounddevice):
        """Test initialization with default parameters."""
        mock_sd, mock_stream = mock_sounddevice
        sensor = NoiseSensor()

        assert sensor.sample_rate == DEFAULT_SAMPLE_RATE
        assert sensor.duration == DEFAULT_DURATION
        assert sensor.freq_range == DEFAULT_FREQ_RANGE
        assert sensor.sensor_type == SensorType.NOISE

        # Verify stream was created with correct parameters
        mock_sd.InputStream.assert_called_once()
        call_kwargs = mock_sd.InputStream.call_args[1]
        assert call_kwargs['device'] == 'adau7002'
        assert call_kwargs['samplerate'] == DEFAULT_SAMPLE_RATE
        assert call_kwargs['channels'] == 1
        assert call_kwargs['dtype'] == 'float32'

        # Verify stream was started
        mock_stream.start.assert_called_once()
        mock_sd.sleep.assert_called_once_with(2000)

        sensor.close()

    def test_init_custom_params(self, mock_sounddevice):
        """Test initialization with custom parameters."""
        mock_sd, _ = mock_sounddevice
        custom_rate = 44_100
        custom_duration = 1.5
        custom_range = (100, 5000)

        sensor = NoiseSensor(
            sample_rate=custom_rate,
            duration=custom_duration,
            freq_range=custom_range
        )

        assert sensor.sample_rate == custom_rate
        assert sensor.duration == custom_duration
        assert sensor.freq_range == custom_range

        # Verify stream was created with custom sample rate
        call_kwargs = mock_sd.InputStream.call_args[1]
        assert call_kwargs['samplerate'] == custom_rate

        sensor.close()


class TestNoiseSensorClose:
    """Tests for NoiseSensor.close() method."""

    def test_close_stops_and_closes_stream(self, noise_sensor, mock_sounddevice):
        """Test that close() properly stops and closes the stream."""
        _mock_sd, mock_stream = mock_sounddevice

        noise_sensor.close()

        mock_stream.stop.assert_called_once()
        mock_stream.close.assert_called_once()

    def test_close_idempotent(self, noise_sensor, mock_sounddevice):
        """Test that calling close() multiple times doesn't cause errors."""
        _mock_sd, mock_stream = mock_sounddevice

        noise_sensor.close()
        noise_sensor.close()  # Should not raise

        # Both calls should have been made
        assert mock_stream.stop.call_count == 2
        assert mock_stream.close.call_count == 2


class TestNoiseSensorRead:
    """Tests for NoiseSensor.read() method."""

    def test_read_returns_sensor_reading(self, noise_sensor):
        """Test that read() returns a SensorReading object."""
        # Mock the _record method to return test data
        test_data = np.random.randn(int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data)

        reading = noise_sensor.read()

        assert isinstance(reading, SensorReading)
        assert reading.sensor_type == SensorType.NOISE
        assert isinstance(reading.timestamp, dt.datetime)
        assert reading.value >= 0  # Mean amplitude should be non-negative

    def test_read_freq_range_validation_nyquist(self, noise_sensor):
        """Test that read() validates frequency range against Nyquist frequency."""
        # Set an invalid frequency range (exceeds Nyquist)
        noise_sensor.freq_range = (30_000, 40_000)

        with pytest.raises(ValueError):
            noise_sensor.read()

    def test_read_freq_range_at_nyquist_limit(self, noise_sensor):
        """Test that read() accepts frequency range at Nyquist limit."""
        # Set frequency range exactly at Nyquist limit
        nyquist = noise_sensor.sample_rate // 2
        noise_sensor.freq_range = (100, nyquist)

        # Mock _record to return data
        test_data = np.random.randn(int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data)

        # Should not raise
        reading = noise_sensor.read()
        assert isinstance(reading, SensorReading)

    def test_read_processes_data_correctly(self, noise_sensor):
        """Test that read() processes audio data correctly."""
        # Create test data with known properties
        # Generate a sine wave at a known frequency within our range
        freq = 1000  # Hz, within default range (400, 3000)
        t = np.linspace(0, DEFAULT_DURATION,
                        int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION),
                        endpoint=False)
        test_data = (0.5 * np.sin(2 * np.pi * freq * t)).astype(np.float32)

        noise_sensor._record = MagicMock(return_value=test_data)

        reading = noise_sensor.read()

        # The mean amplitude should be positive (we have a signal)
        assert reading.value > 0

    def test_read_filters_frequencies(self, noise_sensor):
        """Test that read() correctly filters frequencies outside the configured range."""
        # Save original freq_range and restore after test
        original_range = noise_sensor.freq_range

        # Test 1: Only out-of-range frequencies should produce near-zero reading
        noise_sensor.freq_range = (1000, 3000)
        t = np.linspace(0, DEFAULT_DURATION,
                        int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION),
                        endpoint=False)

        # Only low frequency (below 1000)
        low_freq = 50
        test_data_low = (0.5 * np.sin(2 * np.pi * low_freq * t)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data_low)
        reading_low = noise_sensor.read()
        assert reading_low.value < 50, "Low frequency outside range should be filtered out"

        # Only high frequency (above 3000)
        high_freq = 10_000
        test_data_high = (0.5 * np.sin(2 * np.pi * high_freq * t)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data_high)
        reading_high = noise_sensor.read()
        assert reading_high.value < 50, "High frequency outside range should be filtered out"

        # Test 2: In-range frequency should produce positive reading
        in_range_freq = 2000
        test_data_in = (0.5 * np.sin(2 * np.pi * in_range_freq * t)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data_in)
        reading_in = noise_sensor.read()
        assert reading_in.value > reading_low.value, "In-range frequency should produce positive reading"

        # Restore original range
        noise_sensor.freq_range = original_range


class TestNoiseSensorRecord:
    """Tests for NoiseSensor._record() method."""

    def test_record_reads_correct_number_of_samples(self, noise_sensor, mock_sounddevice):
        """Test that _record() reads the correct number of samples."""
        mock_sd, mock_stream = mock_sounddevice

        # Mock the stream.read to return data
        expected_samples = int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION)
        mock_data = np.random.randn(expected_samples, 1).astype(np.float32)
        mock_stream.read.return_value = (mock_data, False)

        data = noise_sensor._record()

        # Check that read was called with correct number of samples
        call_args = mock_stream.read.call_args[0]
        assert call_args[0] == expected_samples

        # Check that data is squeezed (1D array)
        assert data.ndim == 1
        assert len(data) == expected_samples

    def test_record_handles_overflow(self, noise_sensor, mock_sounddevice):
        """Test that _record() handles audio overflow correctly."""
        mock_sd, mock_stream = mock_sounddevice

        expected_samples = int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION)
        mock_data = np.random.randn(expected_samples, 1).astype(np.float32)
        # Set overflowed to True
        mock_stream.read.return_value = (mock_data, True)

        # Should still return data even with overflow
        data = noise_sensor._record()

        assert data is not None
        assert len(data) == expected_samples


class TestNoiseSensorEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_init_with_zero_duration(self, mock_sounddevice):  # noqa: F841
        """Test initialization with zero duration."""
        sensor = NoiseSensor(duration=0)
        assert sensor.duration == 0
        sensor.close()

    def test_init_with_very_high_sample_rate(self, mock_sounddevice):  # noqa: F841
        """Test initialization with very high sample rate."""
        sensor = NoiseSensor(sample_rate=192_000)
        assert sensor.sample_rate == 192_000
        sensor.close()

    def test_read_with_empty_data(self, noise_sensor):
        """Test read() with empty/zero data."""
        # Return zeros
        test_data = np.zeros(int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION), dtype=np.float32)
        noise_sensor._record = MagicMock(return_value=test_data)

        reading = noise_sensor.read()

        # Mean amplitude of zeros should be 0
        assert reading.value == 0.0

    def test_read_with_all_negative_data(self, noise_sensor):
        """Test read() with all negative data (after DC offset removal)."""
        # Create negative data
        test_data = -np.abs(np.random.randn(int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION))).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data)

        # After DC offset removal, magnitude should be positive
        reading = noise_sensor.read()
        assert reading.value >= 0

    def test_freq_range_reversed(self, noise_sensor):
        """Test read() with reversed frequency range (high < low) raises ValueError."""
        noise_sensor.freq_range = (3000, 400)  # Reversed

        with pytest.raises(ValueError) as exc_info:
            noise_sensor.read()

        assert "low must be less than or equal to high" in str(exc_info.value)

    def test_same_freq_range_boundaries(self, noise_sensor):
        """Test read() with same low and high frequency."""
        # Single frequency point
        noise_sensor.freq_range = (1000, 1000)

        test_data = np.random.randn(int(DEFAULT_SAMPLE_RATE * DEFAULT_DURATION)).astype(np.float32)
        noise_sensor._record = MagicMock(return_value=test_data)

        # Should work - mask will select exactly that frequency bin
        reading = noise_sensor.read()
        assert isinstance(reading, SensorReading)


class TestNoiseSensorConstants:
    """Tests for module constants."""

    def test_freq_low_default(self):
        """Test that FREQ_LOW is set to expected value."""
        assert FREQ_LOW == 400

    def test_freq_high_default(self):
        """Test that FREQ_HIGH is set to expected value."""
        assert FREQ_HIGH == 3_000
