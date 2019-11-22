# Import the ADS1x15 module.
import Adafruit_ADS1x15
#!/usr/bin/python
class Battery():
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115();
        self.voltage = 0;
        self.GAIN = 1;
    def updateMeasurement(self):
        self.voltage = self.adc.read_adc(0, gain=self.GAIN)/1568. #7.4
    def getVoltage(self):
        return self.voltage;
