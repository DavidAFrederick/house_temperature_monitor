#==(Import libraries)=================================
import os
import glob
from datetime import datetime
import time
import csv

# https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
# sudo pip3 install --install-option="--force-pi" Adafruit_DHT

import Adafruit_DHT

from networktables import NetworkTables
import logging  # To see messages from networktables, you must setup logging


#=====================================================
#==(Initialize CONSTANTS)=============================
HVAC_INPUT = 0
HVAC_OUTPUT = 1
WATER_HEATER = 2
TBD = 3

#=====================================================
#==(Initialize variables)=============================

base_dir = '/sys/bus/w1/devices/'
device_folder = []
device_file = []

global DTH_humidity
global DTH_temperature
DTH_humidity = 0
DTH_temperature = 0

#=====================================================
#==(Initialize NetworkTables )========================
NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")
results = sd.putString ("rpi_zero_w_1_temperature", "3.14159")
results = sd.putString ("rpi_zero_w_1_humidity", "3.14159")

logging.basicConfig(level=logging.DEBUG)

#=====================================================

#==(Functions)========================================
def Initialize_the_one_wire_temperature_sensors():
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    device_folder = glob.glob(base_dir + '28*')  # Locate folders that start with 28
    print("Devices: ", device_folder)
    # Creates ['/sys/bus/w1/devices/28-0000068a79af', '/sys/bus/w1/devices/28-0000068a0ad5',
    #          '/sys/bus/w1/devices/28-0000068a292a', '/sys/bus/w1/devices/28-0000068afc05']

    number_of_sensors = len(device_folder)
    print("Found " + str(number_of_sensors) + " Temperature Sensors")

    for sensor in range(number_of_sensors):
        device_file.append(device_folder[sensor] + '/w1_slave')
        # print(read_temp_one_wire_temperature_sensor(device_file[sensor]))

def read_temp_raw_one_wire_temperature_sensor(deviceFile):
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp_one_wire_temperature_sensor(deviceFile):
    lines = read_temp_raw_one_wire_temperature_sensor(deviceFile)
    # Example: lines =  ['3a 01 4b 46 7f ff 06 10 42 : crc=42 YES\n', '3a 01 4b 46 7f ff 06 10 42 t=19625\n']
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw_one_wire_temperature_sensor(deviceFile)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_f = round(temp_f,1)
        return temp_f

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def Read_the_DTH_sensor_temperature() -> int:
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 24 
    DHT_RETRY_TIME = 2
    
    DTH_humidity, DTH_temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, DHT_RETRY_TIME)
    if (DTH_humidity == None) or (DTH_temperature == None):
        print ("Error:  DTH no data")
        DTH_humidity = 0
        DTH_temperature = 0

    DTH_humidity = int(DTH_humidity)
    DTH_temperature  = int(DTH_temperature)
    return DTH_temperature

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def Read_the_DTH_sensor_humidity() -> int:
    DHT_SENSOR = Adafruit_DHT.DHT22
    DHT_PIN = 24 
    DHT_RETRY_TIME = 2
    
    DTH_humidity, DTH_temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN, DHT_RETRY_TIME)
    if (DTH_humidity == None) or (DTH_temperature == None):
        print ("Error:  DTH no data")
        DTH_humidity = 0
        DTH_temperature = 0

    DTH_humidity = int(DTH_humidity)
    DTH_temperature  = int(DTH_temperature)
    return DTH_humidity

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def get_HVAC_input() -> float:
    return read_temp_one_wire_temperature_sensor(device_file[HVAC_INPUT])

def get_HVAC_output() -> float:
    return read_temp_one_wire_temperature_sensor(device_file[HVAC_OUTPUT])

def get_WaterHeater() -> float:
    return read_temp_one_wire_temperature_sensor(device_file[WATER_HEATER])

def get_TBD() -> float:
    return read_temp_one_wire_temperature_sensor(device_file[TBD])

# - - - - - - - - - - - - - - - - - - - - - - - - - - 

def write_header_line():
    with open(output_filename, 'a') as working_file:
        writer = csv.writer(working_file, quoting=csv.QUOTE_ALL)
        writer.writerow(("Date", "Humidifier", "AC Air Out", "WaterHeater", "AC Air In",
                         "Humidity (DHT)", "Temp (DHT)","Remote Humidity (DHT)", "Remote Temp (DHT)"))
    open(output_filename).close()


# tbody   = table body
#  td     = table cell
#  tr     = table row
#  nbsp   = Non-breaking space




def create_web_page (date_time_string, ac_temp_input, ac_temp_output, ac_temp_delta, ac_run_time_current,
              ac_run_time_whole_day, humidity, water_heater_temp, rpi_zero_w_1_humidity, rpi_zero_w_1_temperature):

    page_text = [
    '<h1 style="text-align: left;color:rgb(255, 1, 1); "><strong>System Temperatures (Ver: March 3a, 2025)</strong></h1> \n',
    '<table style="height: 14px; width: 400px; border-collapse: collapse; float: left;" border="0"> \n',
    '<tbody> \n',
    '<tr style="height: 18px;"> \n',
    '<td style="color:rgb(1, 1, 1); width: 60px; height: 18px; text-align: left;"><strong>Last Measurement Date/Time</strong>:</td> \n',
    '<td style="color:rgb(2, 100, 1); width: 70px; height: 18px; border-style: none; text-align: left;"> \n',
    date_time_string,
    '</td >\n',
    '</tr> \n',
    '</tbody> \n',
    '</table> \n',
    '<p>&nbsp;</p> \n',
    '<p>&nbsp;</p> \n',
    '<p><strong>AC Temperatures:</strong></p> \n',
    '<table style="height: 14px; width: 400px; border-collapse: collapse; float: left;" border="0"> \n',
    '<tbody> \n',
    '<tr style="height: 18px;"> \n',
    '<td style="color:rgb(1, 1, 1); width: 60px; height: 18px; text-align: left;"><strong>Output</strong>:</td> \n',
    '<td style="color:rgb(255, 1, 1); width: 70px; height: 18px; border-style: none; text-align: left;">',ac_temp_output, '</td> \n',
    '<td style="color:rgb(1, 1, 1); width: 30px; height: 18px; text-align: left;"><strong>Input</strong>:</td> \n',
    '<td style="color:rgb(255, 1, 1); width: 70px; height: 18px; text-align: left;">', ac_temp_input, '</td> \n',
    '<td style="color:rgb(1, 1, 1); width: 30px; height: 18px; text-align: left;"><strong>Delta</strong>:</td> \n',
    '<td style="color:rgb(255, 1, 1); width: 70px; height: 18px; text-align: left;">',ac_temp_delta,'</td> \n',
    '</tr> \n',
    '</tbody> \n',
    '</table> \n',
    '<p>&nbsp;</p> \n',
    '<p>&nbsp;</p> \n',
    '<p><strong>AC Run time (minutes):</strong></p> \n',
    '<table style="width: 300px; border-collapse: collapse; float: left;" border="0"> \n',
    '<tbody> \n',
    '<tr> \n',
    '<td style="color:rgb(1, 1, 1); width: 70px;"><strong>Current</strong>:</td> \n',
    '<td style="color:rgb(0, 0, 255); width: 60px;">',ac_run_time_current,'</td> \n',
    '<td style="color:rgb(1, 1, 1); width: 70px;"><strong>Today</strong>:</td> \n',
    '<td style="color:rgb(0, 0, 255); width: 60px;">',ac_run_time_whole_day,'</td> \n',
    '</tr> \n',
    '</tbody> \n',
    '</table> \n',
    '<p>&nbsp;</p> \n',
    '<p>&nbsp;</p> \n',
    '<p style="color:rgb(1, 100, 1);"><strong>Humidity:&nbsp;</strong>',humidity,'</p> \n',
    '<p style="color:rgb(1, 100, 1);"><strong>Water Heater Sensor:</strong>&nbsp;', water_heater_temp,'</p> \n',
    '<p>&nbsp;</p> \n',
    '<p style="color:rgb(200, 1, 1);"><strong>RPI_1: Humidity:&nbsp;</strong>',rpi_zero_w_1_humidity,'</p> \n',
    '<p style="color:rgb(200, 1, 1);"><strong>RPI_1: Temperature </strong>&nbsp;', rpi_zero_w_1_temperature,'</p> \n'
    '<img src="temperature_graph.jpg">'
    ]
    
    output_filename = '/var/www/html/index.html'
    with open(output_filename, 'w') as f:
        for line in page_text:
            f.write(line)
            
            
#===================================================================================


# - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - 



#=====================================================
#==(Main program)=====================================

Initialize_the_one_wire_temperature_sensors()

print (" get_HVAC_input:   ", get_HVAC_input())
print (" get_HVAC_output: ", get_HVAC_output())
print (" get_WaterHeater: ", get_WaterHeater())
print (" get_HVAC_input: ", get_TBD())
print (" Get DHT Temp: ", Read_the_DTH_sensor_temperature())
print (" Get DHT Humidty: ", Read_the_DTH_sensor_humidity())

time_to_collect_data = True    # Used to trigger collecting new data each minute
start_new_day =  True

while (time_to_collect_data):
    # Get current time
    print ("Current Time: ")

    # Read sensors

    # Reformat data to needed format

    # Write data to files


    # Files in use
    #  1)  All data files
    #  2)  Last 


    # All Data file
    # Last 24 hours 


    # Create web page template

    # Publish we page
    

    # Check to see if its time to collect data again
    pass
    time_to_collect_data = False



#=====================================================


#==(Wiring Notes)========================================
# Wiring Notes:
# Sensors consist of 4 single-wire thermometers and 1 DHT sensor
# The 4 single wire sensors have the wires parallelled.
# Power = +3.3V on pin 1
# Ground = on pin 6
# Signal (Yellow wire) on pin 7
#
# DHT 
# Power (3.3V) on pin 17
# Signal on pin 18 GPIO pin 24
# Ground on pin 20
#=====================================================


#  sudo systemctl restart temperatureMonitor


#=====================================================
