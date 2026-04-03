import  adafruit_dht 
import board
import time

# import ntcore # The Python NetworkTables library
import networktables
print (f"NT-Client:  Setup: 1")

# scp ./DHT6a.py a@192.168.1.226:/home/a/python


# To see messages from networktables, you can set up logging
import logging
logging.basicConfig(level=logging.DEBUG)
print (f"NT-Client:  Setup: 2")


# Get the default instance of NetworkTables
inst = networktables.NetworkTablesInstance.getDefault()
print (f"NT-Client:  Setup: 3")

# Start a NetworkTables client with a unique name
# Replace TEAM_NUMBER with your FRC team number
inst.startClient("my-python-client") 
#inst.setServerTeam(TEAM_NUMBER)
print (f"NT-Client:  Setup: 4")


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


# rpi_zero_DHT_temperature = 999
# rpi_zero_DHT_humidity = 888
# while True:
#     table.putString("rpi_zero_w_1_temperature",  str(rpi_zero_DHT_temperature))
#     table.putString("rpi_zero_w_1_humidity",     str(rpi_zero_DHT_humidity))
#     print (f"NT-Client:  Setup: 7")


    
#     # Wait before the next update
#     time.sleep(1)
#     # i += 1


#dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=True)

while True:
    try:

        rpi_zero_DHT_temperature = dhtDevice.temperature
        rpi_zero_DHT_humidity = dhtDevice.humidity


        table.putString("rpi_zero_DHT_temperature",  str(rpi_zero_DHT_temperature))
        table.putString("rpi_zero_DHT_humidity",     str(rpi_zero_DHT_humidity))

        print(f"Received rpi_zero_DHT_temperature:{rpi_zero_DHT_temperature}   rpi_zero_DHT_humidity:{rpi_zero_DHT_humidity} ")



        # myValue_publisher.set(dhtDevice.temperature)

        # print(f"Temp: {dhtDevice.temperature:.1f}C, Humidity: {dhtDevice.humidity}%")
        # table.putNumber("rpi_zero_w_1_temperature",dhtDevice.temperature)
        # table.putNumber("rpi_zero_w_1_humidity",dhtDevice.humidity)

    except RuntimeError as e:
        print(e)
    time.sleep(2)

