#!/usr/bin/python
# -*- coding:utf-8 -*-
import threading
from socketIO_client import SocketIO, LoggingNamespace

class Socket(threading.Thread):
    def __init__(self):
        print("Loading Socket Communication...");
        threading.Thread.__init__(self)
        self.socketIO = SocketIO('localhost', 3001, LoggingNamespace)
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('task_rover', self.on_task_response)
        # self.socketIO.on('command', self.on_motors_response)
        print("Loaded Socket Communication");

    def on_connect(self, *args):
        print("Connection Ok...")
    def on_disconnect(*args):
        print('disconnect')
    def on_reconnect(self, *args):
        print('reconnect')
    def on_aaa_response(self, *args):
        print('on_aaa_response', args)

    def on_task_response(self,*args):
        # print('task_rover',args)
        for arg in args:
            data = arg
        data  = json.loads(data)
        print('Data:', str(data['typeTask']))
    def on_bbb_response(*args):
        print('on_bbb_response', args)
    def sendMessage(self,task,data):
        self.socketIO.emit(task, data, self.on_bbb_response)

    def run(self):
        self.socketIO.wait()
