'''Orchestrator for the data pipeline.'''

# Initially, I want to just be able to capture values

import datetime as dt
import sys
import time

from envirospace_monitor import SensorReading, SensorType

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559


try:
    while True:
        light = ltr559.get_lux()
        light_reading = SensorReading(
            timestamp=dt.datetime.now(dt.UTC),
            sensor_type=SensorType.LIGHT,
            value=light
        )
        print(light_reading)
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)
