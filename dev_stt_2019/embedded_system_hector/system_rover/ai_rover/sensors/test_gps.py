#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import time
from Gps import Gps

# ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
gps_sensor = Gps();
gps_sensor.start();
while True:
        # gps_sensor.updateData();
        # print"Coordinates";
        print(gps_sensor.latitude);
        print(gps_sensor.longitude);
        time.sleep(0.5)
        # with open("position.txt","w") as pos:
        #     pos.write("%f,%f\n"%str(gps_sensor.latitude),gps_sensor.longitude );
    # ser.write(received_data)                #transmit data serially
