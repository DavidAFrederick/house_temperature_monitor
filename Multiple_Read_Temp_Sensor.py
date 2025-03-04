#  Updated June 13, 2022 - 
#  Remote update on March 4, 2025
# Test March 2
import os
import glob
import time
from datetime import datetime
import csv

#  sudo systemctl restart temperatureMonitor


# https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
# sudo pip3 install --install-option="--force-pi" Adafruit_DHT

import Adafruit_DHT

import time
from networktables import NetworkTables

# To see messages from networktables, you must setup logging
import logging

logging.basicConfig(level=logging.DEBUG)

NetworkTables.initialize()
sd = NetworkTables.getTable("SmartDashboard")
results = sd.putString ("rpi_zero_w_1_temperature", "3.14159")
results = sd.putString ("rpi_zero_w_1_humidity", "3.14159")
#print ("Result of adding value:", results)


#============================================================
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

daily_ac_total_time_running = 0
ac_run_time_current = 0
current_hour = 0
ac_run_time_whole_day_float = 0
ac_run_time_whole_day_string = "0"
output_filename = '/home/pi/python/BasementTemperatureData.csv'
debug_file_name2 = "/home/pi/python/debug2.txt"
debug_file_name3 = "/home/pi/python/debug3.txt"



# =(Functions)===========================================================
def read_temp_raw(deviceFile):
    f = open(deviceFile, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp(deviceFile):
    lines = read_temp_raw(deviceFile)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(deviceFile)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        temp_f = round(temp_f,1)
        return temp_f

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

# =(End of Functions)===========================================================

# ======================================================================
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24

# name the CSV file for the data log
#output_filename = '/home/pi/python/BasementTemperatureData.csv'
base_dir = '/sys/bus/w1/devices/'
device_folder = []
device_file = []
device_folder = glob.glob(base_dir + '28*')  # Locate folders that start with 28

# print(device_folder)
# Creates ['/sys/bus/w1/devices/28-0000068a79af', '/sys/bus/w1/devices/28-0000068a0ad5',
#          '/sys/bus/w1/devices/28-0000068a292a', '/sys/bus/w1/devices/28-0000068afc05']
number_of_sensors = len(device_folder)
print("Found " + str(number_of_sensors) + " Temperature Sensors")

# Identify each sensor column data name
write_header_line()

for sensor in range(number_of_sensors):
    device_file.append(device_folder[sensor] + '/w1_slave')
    # print(read_temp(device_file[sensor]))

while True:
    currenttime = datetime.now().replace(microsecond=0)
 #   print (currenttime)

    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    print("Humidity: ", humidity, "  Temperature: ", temperature)

    humidity = 99
    temperature = 88
    humidity = int(humidity)
    temperature  = int(temperature)
    
    rpi_zero_w_1_temperature = float ( sd.getString ("rpi_zero_w_1_temperature", "0"))
    rpi_zero_w_1_humidity =    float ( sd.getString ("rpi_zero_w_1_humidity", "0" ) )

    with open(output_filename, 'a') as working_file:
        writer = csv.writer(working_file, quoting=csv.QUOTE_ALL)
        writer.writerow((currenttime, read_temp(device_file[0]), read_temp(device_file[1]),
                         read_temp(device_file[2]), read_temp(device_file[3]), humidity, temperature,
                         rpi_zero_w_1_humidity, rpi_zero_w_1_temperature))
    open(output_filename).close()



    date_time_string            =  str(currenttime)
    ac_temp_input               =  str( read_temp(device_file[3]) )
    ac_temp_output              =  str( read_temp(device_file[1]) )
    ac_temp_delta               =  str(int( read_temp(device_file[3]) - read_temp(device_file[1])) )
    ac_temp_delta_float         =  abs(float(ac_temp_delta))     ###  Added abs
    ac_run_time_current         =  ac_run_time_current
    ac_run_time_whole_day       =  str( ac_run_time_whole_day_float )
    rpi_zero_w_1_temperature_str = str(rpi_zero_w_1_temperature)
    rpi_zero_w_1_humidity_str   = str(rpi_zero_w_1_humidity)
    
    humidity                    =  str(humidity)
    water_heater_temp           =  str(read_temp(device_file[2]))

                                                                     ####  Add code to differentiate heating and cooling
    if ac_temp_delta_float > 14:                                     ####   Changed this from 20 to 14
        ac_run_time_current = ac_run_time_current + 1
        ac_run_time_whole_day_float = ac_run_time_whole_day_float + 1
        ac_run_time_whole_day_string = str(ac_run_time_whole_day_float)
        ac_run_time_current_string = str(ac_run_time_current)
        string1 = "AC is running: current: "  + str(ac_run_time_current_string) + "\n"
        string2 = "AC is running: day: "      + str(ac_run_time_whole_day) + "\n"
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
        file3.write(string1 + "  current hour: "  + str(current_hour) + " whole day: " + str(ac_run_time_whole_day)  + "\n")
        ac_run_time_whole_day_float = 0
        file3.close()

        # new day
    
    
#    if datetime.hour():
#        continue

    create_web_page (date_time_string, ac_temp_input, ac_temp_output, ac_temp_delta, ac_run_time_current_string,
              ac_run_time_whole_day_string, humidity, water_heater_temp,
              rpi_zero_w_1_humidity_str, rpi_zero_w_1_temperature_str)

#    print (currenttime)
    time.sleep(51)        #### Reduce by 8 seconds since not running often enough  ## CHANGED FROM 59 to 51



# import matplotlib.pyplot as plt
# import numpy as np

# x = np.loadtxt('testdata2.cvs') #for comma separated values

# plt.plot(x, label='Data from file')
# plt.xlabel('X-axis label')
# plt.title('Plot of data from file')
# plt.legend()
# # plt.show()

# plt.savefig('sine_wave.png', dpi=300, bbox_inches='tight')
# plt.close()

