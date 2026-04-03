import time
import networktables

# scp ./DHT6a.py a@192.168.1.226:/home/a/python


# To see messages from networktables, you can set up logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Get the default instance of NetworkTables
# inst = networktables.NetworkTablesInstance.getDefault()
inst = networktables.NetworkTablesInstance.getDefault()

# Start a NetworkTables client with a unique name
# Replace TEAM_NUMBER with your FRC team number
# inst.startClient4("my-python-client") 
inst.startClient("my-python-client") 
#inst.setServerTeam(TEAM_NUMBER)

# Alternatively, set a specific IP address if needed:
#inst.setServer("192.168.1.224", networktables.NetworkTablesInstance.kDefaultPort4) 
inst.setServer("192.168.1.224") 

# Get a reference to the table named "datatable"
table = inst.getTable("SmartDashboard")

# Publish a topic within the table (e.g., "myValue") and specify its type (e.g., double)
# Publishers should be created once during initialization
#myValue_publisher = table.getDoubleTopic("rpi_zero_w_1_temperature").publish()
myvalue = 12.345
myValue_publisher = table.getNumber("rpi_zero_w_1_temperature",myvalue)

i = 0
t = 0
while True:
    print(f"Published myValue: {i}")
    myvalue = i
    myValue_publisher = table.putNumber("rpi_zero_w_1_temperature",myvalue)
    t = table.getNumber('robotTime', 333)
    print (f"T: {t}")
    time.sleep(1)
    i += 1

