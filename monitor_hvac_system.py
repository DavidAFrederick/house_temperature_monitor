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

HVAC_INPUT   = 3
HVAC_OUTPUT  = 1
WATER_HEATER = 2
HUMIDIFER    = 0

# Device 0   Humidifier
# Device 1   AC Out
# Device 2   Water heater
# Device 3   AC In

#=====================================================
#==(Initialize variables)=============================

base_dir = '/sys/bus/w1/devices/'
device_folder = []
device_file = []

global DTH_humidity
global DTH_temperature
DTH_humidity = 0
DTH_temperature = 0

daily_ac_total_time_running = 0
ac_run_time_current = 0
current_hour = 0
ac_run_time_whole_day_float = 0
ac_run_time_whole_day_string = "0"
output_filename = '/home/pi/python/BasementTemperatureData2.csv'
debug_file_name2 = "/home/pi/python/debug22.txt"
debug_file_name3 = "/home/pi/python/debug32.txt"
web_server_page_filename = '/var/www/html/index.html'

rpi_zero_w_1_temperature = 0
rpi_zero_w_1_humidity =    0
date_time_string = " "
currenttime = datetime.now().replace(microsecond=0)

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
    DHT_RETRY_TIME = 6
    
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

def get_Outside() -> float:
    return read_temp_one_wire_temperature_sensor(device_file[HUMIDIFER])

# - - - - - - - - - - - - - - - - - - - - - - - - - - 

def write_header_line():
    with open(output_filename, 'a') as working_file:
        writer = csv.writer(working_file, quoting=csv.QUOTE_ALL)
        writer.writerow(("Date", "Outside", "AC Air Out", "WaterHeater", "AC Air In",
                         "Humidity (DHT)", "Temp (DHT)","Remote Humidity (DHT)", "Remote Temp (DHT)"))
    open(output_filename).close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def write_row_of_data_to_CSV():
    with open(output_filename, 'a') as working_file:
        writer = csv.writer(working_file, quoting=csv.QUOTE_ALL)
        writer.writerow((currenttime, get_Outside(), get_HVAC_output(), get_WaterHeater(), get_HVAC_input(), humidity_str, temperature_str,
                         rpi_zero_w_1_humidity_str, rpi_zero_w_1_temperature))
    open(output_filename).close()

# - - - - - - - - - - - - - - - - - - - - - - - - - - 

# tbody   = table body
#  td     = table cell
#  tr     = table row
#  nbsp   = Non-breaking space


def create_web_page (date_time_string, ac_temp_input, ac_temp_output, ac_temp_delta, ac_run_time_current,
              ac_run_time_whole_day, humidity, water_heater_temp, rpi_zero_w_1_humidity, rpi_zero_w_1_temperature):
        
    page_text = [
    '<h1 style="text-align: left;color:rgb(255, 1, 1); "><strong>System Temperatures (Ver: March 10, 2025)</strong></h1> \n',
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

    '<table style="height: 14px; width: 400px; border-collapse: collapse; float: left;" border="0"> \n',
    '<tbody> \n',
    '<tr style="height: 18px;"> \n',
    '<td style="color:rgb(1, 1, 1); width: 60px; height: 18px; text-align: left;"><strong>Outside Temperature</strong>:</td> \n',
    '<td style="color:rgb(2, 100, 1); width: 70px; height: 18px; border-style: none; text-align: left;"> \n',
    ac_temp_output_str,
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
    '<p style="color:rgb(1, 100, 1);"><strong>DHT Humidity:&nbsp;</strong>',humidity,'</p> \n',
    '<p style="color:rgb(1, 100, 1);"><strong>DTH Temperature:</strong>&nbsp;', temperature_str,'</p> \n',
    '<p>&nbsp;</p> \n',
    '<p style="color:rgb(200, 1, 1);"><strong>RPI_1: Humidity:&nbsp;</strong>',rpi_zero_w_1_humidity,'</p> \n',
    '<p style="color:rgb(200, 1, 1);"><strong>RPI_1: Temperature </strong>&nbsp;', rpi_zero_w_1_temperature,'</p> \n'
    '<img src="temperature_graph.jpg">'
    ]
    
    with open(web_server_page_filename, 'w') as f:
        for line in page_text:
            f.write(line)
            
            
#===================================================================================


# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def print_sensors():
    print (" get_HVAC_input:   ", get_HVAC_input())
    print (" get_HVAC_output: ", get_HVAC_output())
    print (" get_WaterHeater: ", get_WaterHeater())
    print (" get_Outside: ", get_Outside())
    print (" Get DHT Temp: ", Read_the_DTH_sensor_temperature())
    print (" Get DHT Humidty: ", Read_the_DTH_sensor_humidity())

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
def get_and_print_current_time():
    # Get current time
    global date_time_string
    currenttime = datetime.now().replace(microsecond=0)
    date_time_string = str(currenttime)
    print ("Current Time: ", currenttime)
    print ("date_time_string: ", date_time_string)

# - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Read the remote sensor
def  read_remote_sensors():
    rpi_zero_w_1_temperature = float ( sd.getString ("rpi_zero_w_1_temperature", "0"))
    rpi_zero_w_1_humidity =    float ( sd.getString ("rpi_zero_w_1_humidity", "0" ) )

# - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - 


# - - - - - - - - - - - - - - - - - - - - - - - - - - 



#=====================================================
#==(Main program)=====================================
get_and_print_current_time()
Initialize_the_one_wire_temperature_sensors()
print_sensors()


time_to_collect_data = True    # Used to trigger collecting new data each minute
start_new_day =  True

while (time_to_collect_data):

    get_and_print_current_time()
    read_remote_sensors()

    # Read the sensors and Reformat data to needed format
    ac_temp_input_str               =  str( get_HVAC_input())
    ac_temp_output_str              =  str( get_HVAC_output())
    ac_temp_delta_float             =  abs(int(  get_HVAC_output() - get_HVAC_input()   ))  
    ac_temp_delta_str               =  str(ac_temp_delta_float) 
    water_heater_temp_str           =  str(get_WaterHeater())
    humidity_str                    =  str(Read_the_DTH_sensor_humidity())
    temperature_str                 =  str(Read_the_DTH_sensor_temperature())

    ac_run_time_current_str         =  str(ac_run_time_current)
    ac_run_time_whole_day_str       =  str(ac_run_time_whole_day_float)
    rpi_zero_w_1_temperature_str    =  str(rpi_zero_w_1_temperature)
    rpi_zero_w_1_humidity_str       =  str(rpi_zero_w_1_humidity)


    # Files in use
    #  1)  All data files
    #  2)  Last 


    # All Data file
    # Last 24 hours 

                                                                         ####  Add code to differentiate heating and cooling
    if ac_temp_delta_float > 14:                                     ####   Changed this from 20 to 14
        ac_run_time_current = ac_run_time_current + 1
        ac_run_time_whole_day_float = ac_run_time_whole_day_float + 1
        ac_run_time_whole_day_string = str(ac_run_time_whole_day_float)
        ac_run_time_current_string = str(ac_run_time_current)
        string1 = "AC is running: current: "  + ac_run_time_current_string + "\n"
        string2 = "AC is running: day: "      + ac_run_time_whole_day_string + "\n"
        file1 = open(debug_file_name2, "a")
        file1.write(date_time_string + "\n")
        file1.write(string1)
        file1.write(string2)
        file1.close()
    else:
        ac_run_time_current = 0
        ac_run_time_current_string = str(ac_run_time_current)

    previous_hour = current_hour
    current_hour = int(datetime.now().hour)
    
    if (current_hour == 5 ) and (previous_hour != current_hour):    #### Restarts counter at 3:00 AM   CHANGED TO 5:00 AM
        string1 = "Day Roll Over "
        file3 = open(debug_file_name3, "a")
        file3.write(date_time_string + "\n")
        file3.write(string1 + "  current hour: "  + str(current_hour) + " whole day: " + ac_run_time_whole_day_str  + "\n")
        ac_run_time_whole_day_float = 0
        file3.close()

        # new day
    
    
#    if datetime.hour():
#        continue


    # Write data to files
    write_header_line()
    write_row_of_data_to_CSV()

    # Create web page template
    create_web_page(
        date_time_string, 
        ac_temp_input_str, 
        ac_temp_output_str, 
        ac_temp_delta_str, 
        ac_run_time_current_str,
        ac_run_time_whole_day_str, 
        humidity_str, 
        temperature_str,   #  fix
        rpi_zero_w_1_humidity_str, 
        rpi_zero_w_1_temperature_str
    )
    

    # Check to see if its time to collect data again
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
