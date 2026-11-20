"""Unit tests for the LightSensor class.

These tests mock the ltr559 module to test the LightSensor
without requiring actual LTR559 hardware.
"""

import datetime as dt
from unittest.mock import MagicMock, patch

import pytest

from envirospace_monitor.sensors.base import SensorReading, SensorType
from envirospace_monitor.sensors.light import LightSensor


@pytest.fixture
def mock_ltr559():
    """Fixture to mock the ltr559 module."""
    with patch('envirospace_monitor.sensors.light.LTR559') as mock_ltr_class:
        mock_sensor = MagicMock()
        mock_ltr_class.return_value = mock_sensor
        yield mock_ltr_class, mock_sensor


@pytest.fixture
def light_sensor(mock_ltr559):
    """Fixture to create a LightSensor with mocked ltr559."""
    sensor = LightSensor()
    yield sensor


class TestLightSensorInit:
    """Tests for LightSensor initialization."""

    def test_init_creates_ltr559_instance(self, mock_ltr559):
        """Test that __init__ creates an LTR559 instance."""
        mock_ltr_class, mock_sensor = mock_ltr559

        sensor = LightSensor()

        # Verify LTR559 was instantiated
        mock_ltr_class.assert_called_once()
        assert sensor._ltr559 is mock_sensor

        # Verify first reading was discarded
        mock_sensor.get_lux.assert_called_once()

        sensor._ltr559 = None

    def test_sensor_type_is_light(self, light_sensor):
        """Test that sensor_type is LIGHT."""
        assert light_sensor.sensor_type == SensorType.LIGHT


class TestLightSensorRead:
    """Tests for LightSensor.read() method."""

    def test_read_returns_sensor_reading(self, mock_ltr559):
        """Test that read() returns a SensorReading object."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        # Setup mock to return a lux value
        mock_sensor.get_lux.return_value = 123.45

        sensor = LightSensor()
        reading = sensor.read()

        assert isinstance(reading, SensorReading)
        assert reading.sensor_type == SensorType.LIGHT
        assert isinstance(reading.timestamp, dt.datetime)
        assert reading.value == 123.45

    def test_read_returns_positive_lux(self, mock_ltr559):
        """Test reading a positive lux value."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 500.0
        sensor = LightSensor()
        reading = sensor.read()

        assert reading.value == 500.0
        assert reading.unit == "Lux"

    def test_read_returns_zero_lux(self, mock_ltr559):
        """Test reading zero lux (complete darkness)."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 0.0
        sensor = LightSensor()
        reading = sensor.read()

        assert reading.value == 0.0

    def test_read_returns_very_high_lux(self, mock_ltr559):
        """Test reading a very high lux value (bright sunlight)."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 100_000.0
        sensor = LightSensor()
        reading = sensor.read()

        assert reading.value == 100_000.0

    def test_read_calls_get_lux(self, mock_ltr559):
        """Test that read() calls get_lux() on the LTR559 instance."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        # Create sensor - first call happens in __init__
        sensor = LightSensor()
        initial_call_count = mock_sensor.get_lux.call_count
        mock_sensor.get_lux.return_value = 100.0

        sensor.read()

        # Should have been called once more (in addition to init call)
        assert mock_sensor.get_lux.call_count == initial_call_count + 1

    def test_read_timestamp_is_recent(self, mock_ltr559):
        """Test that reading timestamp is recent (within last second)."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        before = dt.datetime.now(dt.UTC)
        mock_sensor.get_lux.return_value = 100.0
        sensor = LightSensor()
        reading = sensor.read()
        after = dt.datetime.now(dt.UTC)

        assert before <= reading.timestamp <= after

    def test_read_to_dict(self, mock_ltr559):
        """Test that the reading can be converted to a dictionary."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 250.5
        sensor = LightSensor()
        reading = sensor.read()

        result = reading.to_dict()

        assert result['sensor_type'] == 'light'
        assert result['value'] == 250.5
        assert result['unit'] == 'Lux'
        assert 'timestamp' in result


class TestLightSensorEdgeCases:
    """Tests for edge cases and error conditions."""

    def test_read_with_negative_lux(self, mock_ltr559):
        """Test reading a negative lux value (sensor error)."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        # In reality, lux shouldn't be negative, but test handles it
        mock_sensor.get_lux.return_value = -10.0
        sensor = LightSensor()
        reading = sensor.read()

        assert reading.value == -10.0

    def test_read_with_float_lux(self, mock_ltr559):
        """Test reading a float lux value with decimals."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 123.456789
        sensor = LightSensor()
        reading = sensor.read()

        assert reading.value == 123.456789
        assert isinstance(reading.value, float)

    def test_multiple_reads(self, mock_ltr559):
        """Test multiple consecutive reads."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        # Setup sequence of lux values - first consumed by __init__, rest by reads
        # Need 5 values: 1 for init + 4 for reads
        mock_sensor.get_lux.side_effect = [None, 50.0, 100.0, 150.0, 200.0]

        sensor = LightSensor()
        readings = [sensor.read() for _ in range(4)]

        assert len(readings) == 4
        assert readings[0].value == 50.0
        assert readings[1].value == 100.0
        assert readings[2].value == 150.0
        assert readings[3].value == 200.0


class TestLightSensorIntegration:
    """Integration-style tests with mocked sensor."""

    def test_sensor_reading_str_representation(self, mock_ltr559):
        """Test the string representation of a SensorReading."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 300.0
        sensor = LightSensor()
        reading = sensor.read()

        str_repr = str(reading)

        assert 'light' in str_repr.lower()
        assert '300.0' in str_repr
        assert 'Lux' in str_repr

    def test_read_consistency(self, mock_ltr559):
        """Test that consecutive reads with same lux value are consistent."""
        _mock_ltr_class, mock_sensor = mock_ltr559

        mock_sensor.get_lux.return_value = 750.0

        sensor = LightSensor()
        reading1 = sensor.read()
        reading2 = sensor.read()

        assert reading1.value == reading2.value
        assert reading1.sensor_type == reading2.sensor_type
        assert reading1.unit == reading2.unit
