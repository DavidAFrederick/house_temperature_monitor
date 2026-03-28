## https://www.instructables.com/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/

#Libraries
# import Adafruit_DHT as dht
# import adafruit_dht as dht
# from time import sleep
# #Set DATA pin
# DHT = 4
# while True:
#     #Read Temp and Hum from DHT22
#     h,t = dht.read_retry(dht.DHT22, DHT)
#     #Print Temperature and Humidity on Shell window
#     print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(t,h))
#     sleep(5) #Wait 5 seconds and read again



import time, board, adafruit_dht
dhtDevice = adafruit_dht.DHT22(board.D3)
while True:
    try:
        print(f"Temp: {dhtDevice.temperature:.1f}C, Humidity: {dhtDevice.humidity}%")
    except RuntimeError as e:
        print(e)
    time.sleep(2)
