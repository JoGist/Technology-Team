#!/usr/bin/python
# -*- coding:utf-8 -*-
from Socket import Socket

class Sender(threading.Thread):
    def __init__(self):
        self.socket = Socket();
        
    def sendMessage(self,task,data):
        self.socketIO.emit(task, data, self.on_bbb_response)

    def run(self):
        self.socketIO.wait()
