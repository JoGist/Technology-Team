#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import time
import threading
import csv

class Gps(threading.Thread):
    def __init__(self):
        print("Loading Gps Sensor...");
        threading.Thread.__init__(self)
        self.ser = serial.Serial ("/dev/ttyS0", 9600)    #Open port with baud rate
        self.latitude = 41.892907;
        self.longitude = 12.493235;
        # 41.892907, 12.493235
        # 41.894056, 12.494044    1)
        self.status = False;
        print("Loaded Gps Sensor");
    def updateData(self):
        try:
            # received_data = self.ser.readline()
            line = []
            while True:
                # print self.ser.read();
                for c in self.ser.read():
                    line.append(c)
                    if c == '\n':
                        print("Line: " + ''.join(line))
                        line = []
                        break
        except:
            print("ERROR");
    def run(self):
        time.sleep(1);
        line = []
        k=0;
        while True:
            try:
                for c in self.ser.read():
                    line.append(c)
                    if c == '\n':
                        k=k+1;
                        received_data = "".join(line);
                        # print("Line: " + received_data)
                        if (received_data.startswith('$GPRMC')):
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
                    # time.sleep(0.05);
            except:
                self.status = False;

    def getData(self):
        data = {};
        data['longitude']=self.longitude;
        data['latitude']=self.latitude;
        return data;
    def readTargetData(self,file):
        file = 'data_gps_target.csv';
        with open(file) as csv_file:
            # csv_reader = csv.reader(csv_file, delimiter=',')
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                print(row)
                line_count += 1
            # print(f'Processed {line_count} lines.')
            print(line_count);
    def writeTargetData(self,file):
        # file = 'data_gps_target.csv';
        with open(file, mode='w') as csv_file:
            fieldnames = ['name', 'longitude', 'latitude']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'number': '0','name': 'Spaccio', 'longitude': 12.493626, 'latitude': 41.89639})
            writer.writerow({'number': '1','name': 'Colosseo', 'longitude': 12.492629, 'latitude': 41.896467})
            writer.writerow({'number': '2','name': 'Colle Oppio', 'longitude': 12.495735, 'latitude': 41.892606})
            writer.writerow({'number': '3','name': 'Fauno', 'longitude': 12.492930, 'latitude': 41.892887})
            writer.writerow({'number': '4','name': 'Pozzo Chiostro', 'longitude': 12.493300, 'latitude': 41.893505})
    def getTargetData(self,file,position):
        # file = 'data_gps_target.csv';
        with open(file) as csv_file:
            # csv_reader = csv.reader(csv_file, delimiter=',')
            csv_reader = csv.DictReader(csv_file)
            line_count = 0
            for row in csv_reader:
                if(line_count == position):
                    return row
                line_count += 1
            # print(f'Processed {line_count} lines.')
            # print(line_count);
