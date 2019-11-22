#!/usr/bin/python
# -*- coding:utf-8 -*-
from __future__ import print_function
import socket
import threading,json
import time
from RF24 import *

millis = lambda: int(round(time.time() * 1000))

class Antenna(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        print("Loading Antenna Communication...");

        self.radio = RF24(RPI_BPLUS_GPIO_J8_22, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

        self.pipes = [0xF0F0F0F0E1, 0xF0F0F0F0D2]
        self.radio.begin()
        self.radio.enableDynamicPayloads()
        self.radio.setRetries(5,15)
        self.radio.setDataRate(RF24_250KBPS);
        # self.radio.printDetails()

        self.radio.openWritingPipe(self.pipes[0])
        self.radio.openReadingPipe(1,self.pipes[1])
        self.payload_size = 32;
        self.dataMessage1 = "0;0.0;0.0;0.0;0.0";
        self.dataMessage2 = "0;0.0;0.0;0.0;0.0";
        self.dataMessage3 = "0;0.0;0.0;0.0;0.0";
        self.dataMessage4 = "0;0.0;0.0;0.0;0.0";
        self.dataMessage5 = "0;0.0;0.0;0.0;0.0";
        self.dataMessage6 = "0;0.0;0.0;0.0;0.0";
        self.dataMessageReceived = "0";
        print("Loaded Antenna Communication");

    def updateDataMessage1(self,dataMessage1):
        self.dataMessage1 = dataMessage1;
    def updateDataMessage2(self,dataMessage2):
        self.dataMessage2 = dataMessage2;
    def updateDataMessage3(self,dataMessage3):
        self.dataMessage3 = dataMessage3;
    def updateDataMessage4(self,dataMessage4):
        self.dataMessage4 = dataMessage4;
    def updateDataMessage5(self,dataMessage5):
        self.dataMessage5 = dataMessage5;
    def updateDataMessage6(self,dataMessage6):
        self.dataMessage6 = dataMessage6;

    def sendMessage(self,data):
        self.radio.stopListening()
        data = str.encode(str(data));
        self.radio.write(data[:self.payload_size])
        # print(data);
    def receiveMessage(self):
        len = self.radio.getDynamicPayloadSize()
        receive_payload = self.radio.read(len)
        self.dataMessageReceived = receive_payload.decode('utf-8');
        # print(self.dataMessageReceived);

    def run(self):
        while(True):
            self.sendMessage(self.dataMessage1);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();

            self.sendMessage(self.dataMessage2);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();

            self.sendMessage(self.dataMessage3);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();

            self.sendMessage(self.dataMessage4);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();

            self.sendMessage(self.dataMessage5);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();

            self.sendMessage(self.dataMessage6);
            self.radio.startListening()

            started_waiting_at = millis()
            timeout = False
            while (not self.radio.available()) and (not timeout):
                if (millis() - started_waiting_at) > 50:
                    timeout = True

            if (timeout == False):
                self.receiveMessage();


            time.sleep(0.1);
