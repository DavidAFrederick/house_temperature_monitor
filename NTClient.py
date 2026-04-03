import time
import networktables
print (f"NT-Client:  Setup: 1")


# scp ./DHT6a.py a@192.168.1.226:/home/a/python


# To see messages from networktables, you can set up logging
import logging
logging.basicConfig(level=logging.DEBUG)
print (f"NT-Client:  Setup: 2")

# Get the default instance of NetworkTables
# inst = networktables.NetworkTablesInstance.getDefault()
inst = networktables.NetworkTablesInstance.getDefault()
print (f"NT-Client:  Setup: 3")

# Start a NetworkTables client with a unique name
# Replace TEAM_NUMBER with your FRC team number
# inst.startClient4("my-python-client") 
inst.startClient("my-python-client") 
print (f"NT-Client:  Setup: 4")
#inst.setServerTeam(TEAM_NUMBER)

# Alternatively, set a specific IP address if needed:
#inst.setServer("192.168.1.224", networktables.NetworkTablesInstance.kDefaultPort4) 
inst.setServer("192.168.1.224") 
print (f"NT-Client:  Setup: 5")

# Get a reference to the table named "datatable"
table = inst.getTable("SmartDashboard")
print (f"NT-Client:  Setup: 6")

# Publish a topic within the table (e.g., "myValue") and specify its type (e.g., double)
# Publishers should be created once during initialization
#myValue_publisher = table.getDoubleTopic("rpi_zero_w_1_temperature").publish()
# myvalue = "12.345"
# myValue_publisher = table.getNumber("rpi_zero_w_1_temperature",myvalue)
# print (f"NT-Client:  Setup: 7")

myvalue = 34

while True:

    myvalue = myvalue + 1
    table.putString("rpi_zero_w_1_temperature",str(myvalue))
    # myValue_publisher = table.putString("rpi_zero_w_1_temperature",str(myvalue))
    print (f"NT-Client:  Setup: 7")
    time.sleep(1)
    