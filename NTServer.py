import time
from datetime import datetime

from networktables import NetworkTables
print (f"NT-Server:  Setup: 1")

# 1. Initialize NetworkTables as the server
# This makes this script the central broker
NetworkTables.initialize()
print (f"NT-Server:  Setup: 2")

#-------------------------------------------------------------------------
# Optional: Set up a listener to see when clients connect
def connectionListener(connected, info):
    print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)
print (f"NT-Server:  Setup: 3")
#-------------------------------------------------------------------------


# 2. Get a table
sd = NetworkTables.getTable('SmartDashboard')
print (f"NT-Server:  Setup: 4")

i = 0
while True:
    # 3. Publish data
    # i += 1
    # sd.putNumber('robotTime', i)
    # print (f"NT-Server:  Setup: 5")

    rpi_zero_DHT_temperature = sd.getString('rpi_zero_DHT_temperature',"3.1")
    rpi_zero_DHT_humidity =    sd.getString("rpi_zero_DHT_humidity",   "3.4")

    
    print(f"Received rpi_zero_DHT_temperature:{rpi_zero_DHT_temperature}   rpi_zero_DHT_humidity:{rpi_zero_DHT_humidity} ")

    currenttime = datetime.now().replace(microsecond=0)
    date_time_string = str(currenttime)
    print ("Current Time: ", currenttime)
    time.sleep(1) # Publish at 1Hz
