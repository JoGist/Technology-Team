#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import time
import threading

class Gps(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
        self.latitude = 500;
        self.longitude = 500;
        self.status = False;
    def updateData(self):
        print("update2")
        try:
            # received_data = self.ser.readline()
            line = []
            while true:
                # print self.ser.read();
                for c in self.ser.read():
                    line.append(c)
                    if c == '\n':
                        print("Line: " + ''.join(line))
                        line = []
                        break
            # words = received_data.split("\n")
            # print(words)
            # if (words[0].startswith( '$GPRMC')):
            #     data = words[0].split(",")
            #     if(data[2] == "A"):
            #         self.latitude = (int(data[3][:2]) + float(data[3][2:])/60);
            #         self.longitude =(int(data[5][:3]) + float(data[5][3:])/60);
            #         self.status = True;
            #     else:
            #         self.status = False;
            # else:
            #     self.status = False;
            #     # print(data[3],data[5])
            # time.sleep(0.05);
        except:
            print("ERROR");
    def run(self):
        line = []
        while True:
            for c in self.ser.read():
                line.append(c)
                if c == '\n':
                    received_data = "".join(line);
                    # print("Line: " + received_data)
                    if (received_data.startswith( '$GPRMC')):
                        data = received_data.split(",")
                        if(data[2] == "A"):
                            self.latitude = (int(data[3][:2]) + float(data[3][2:])/60);
                            self.longitude =(int(data[5][:3]) + float(data[5][3:])/60);
                            # print(self.latitude);
                            # print(self.longitude);
                            self.status = True;
                        else:
                            self.status = False;
                    else:
                        self.status = False;
                    line = []
                    break
            # received_data = self.ser.readline()
            # words = received_data.split("\n")
            # print(received_data)
            # if (words[0].startswith( '$GPRMC')):
            #     data = words[0].split(",")
            #     if(data[2] == "A"):
            #         self.latitude = (int(data[3][:2]) + float(data[3][2:])/60);
            #         self.longitude =(int(data[5][:3]) + float(data[5][3:])/60);
            #         # print(self.latitude);
            #         # print(self.longitude);
            #         self.status = True;
            #     else:
            #         self.status = False;
            # else:
            #     self.status = False;
                # print(data[3],data[5])
            # time.sleep(1);

    def getData(self):
        data = {};
        data['longitude']=self.longitude;
        data['latitude']=self.latitude;
        return data;
