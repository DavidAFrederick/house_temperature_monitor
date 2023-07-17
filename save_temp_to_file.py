pi@raspberrypi:~ $ cat save_temp_sensor.py 

import glob
import time
import datetime

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'




def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def write_to_file(text_to_write):
    text_to_write = text_to_write + "\n"
    output_filename = open ("/home/pi/python/TemperatureData.txt","a")
    output_filename.writelines(text_to_write);
    output_filename.close()


while True:
    now = datetime.datetime.now()
    print(now.time(), " ", read_temp())
    write_to_file (str(now.time()) + " " + str(read_temp()))
    time.sleep(60)
