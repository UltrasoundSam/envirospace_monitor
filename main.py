'''Orchestrator for the data pipeline.'''

# Initially, I want to just be able to capture values

import sys
import time

try:
    # Transitional fix for breaking change in LTR559
    from ltr559 import LTR559
    ltr559 = LTR559()
except ImportError:
    import ltr559


try:
    while True:
        light = ltr559.get_lux()
        print(f"Light: {light} Lux")
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")
    sys.exit(0)