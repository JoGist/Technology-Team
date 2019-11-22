# Import the ADS1x15 module.
import Adafruit_ADS1x15
import time
import threading

#!/usr/bin/python
class Battery(threading.Thread):
    def __init__(self):
        print("Loading Battery Sensor...");
        threading.Thread.__init__(self)
        self.adc = Adafruit_ADS1x15.ADS1115();
        self.voltage = 0;
        self.GAIN = 1;
        print("Loaded Battery Sensor");
    def updateMeasurement(self):
        self.voltage = self.adc.read_adc(0, gain=self.GAIN)/1568. #7.4
    def getVoltage(self):
        return self.voltage;
    def run(self):
        while True:
            try:
                self.voltage = self.adc.read_adc(0, gain=self.GAIN)/1568. #7.4
                time.sleep(0.01);
                status = True;
            except:
                # print("Not Loaded");
                time.sleep(8);
                status = False;
