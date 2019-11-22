#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial
import time
import threading
import csv
from datetime import datetime

class BlackBox(threading.Thread):
    def __init__(self,fieldnames=["test"],reg=True):
        print("Loading BlackBox Sensor...");
        threading.Thread.__init__(self)
        self.reg = reg;
        self.folder = "black_box"
        self.nameFile = "black_box"
        self.format = ".csv"
        now = datetime.now();
        self.dt_string = now.strftime("%d_%m_%Y_%H_%M_%S");
        self.fieldnames = fieldnames;
        self.data  = {};
        self.isUpdatedData = False;
        with open(self.getFilePath(), mode='w') as csv_file:
            # fieldnames = ['name', 'longitude', 'latitude']
            writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
            writer.writeheader()
        print("Loaded BlackBox Sensor");
    def run(self):
        try:
            with open(self.getFilePath(), mode='a') as csv_file:
                fieldnames = ['name', 'longitude', 'latitude']
                writer = csv.DictWriter(csv_file, fieldnames=self.fieldnames)
                while True:
                    time.sleep(0.1);
                    if(self.isUpdatedData):
                        writer.writerow(self.data);
                        self.isUpdatedData = False;
        except:
            print("ERROR");

    def getFilePath(self):
        if(self.reg):
            return self.folder + "/" + self.nameFile + "_" + self.dt_string + self.format;
        else:
            return self.folder + "/" + self.nameFile + self.format;
    def updateData(self,data):
        self.data = data;
        self.isUpdatedData = True;
