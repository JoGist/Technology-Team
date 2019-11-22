#!/usr/bin/python
# -*- coding:utf-8 -*-
import socket
import threading,json

class SocketUDP(threading.Thread):
    def __init__(self,addressGround):
        threading.Thread.__init__(self)
        print("Loading SocketUDP Communication...");
        # Create a TCP/IP socket
        # self.serverAddressPort   = ("192.168.1.119", 20001)
        self.serverAddressPort   = ("172.20.10.3", 20001)
        self.bufferSize          = 1024
        self.sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.task = 1;
        # self.addressGround = addressGround;
        # self.port = 10000;

        print("Loaded SocketUDP Communication");
    def sendMessage(self,data):
        sent = self.sock.sendto(data.encode(), self.serverAddressPort)
        # print(sent);
    def run(self):
        while(True):
            msgFromServer = self.sock.recvfrom(self.bufferSize)
            message = msgFromServer[0];
            data = json.loads(message);

            # print(data);
            # print(data['typeTask']);
            task = data['typeTask'];
            if(task == "start_mission"):
                self.task = 10;
            print(self.task);
