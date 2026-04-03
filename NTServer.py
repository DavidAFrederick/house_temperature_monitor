import time
from networktables import NetworkTables

# 1. Initialize NetworkTables as the server
# This makes this script the central broker
NetworkTables.initialize()

# Optional: Set up a listener to see when clients connect
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# 2. Get a table
sd = NetworkTables.getTable('SmartDashboard')

i = 0
while True:
    # 3. Publish data
    i += 1
    sd.putNumber('robotTime', i)
    sd.putBoolean('enabled', True)
    T = sd.getNumber('rpi_zero_w_1_temperature',2.22)
    
    print(f"Published: {i}    T:{T}")
    time.sleep(1) # Publish at 1Hz
