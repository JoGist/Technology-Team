#Import Library
import RPi.GPIO as GPIO

#naming convention
GPIO.setmode(GPIO.BCM)
#GPIO warning messages
GPIO.setwarnings(False)

class Led():
    def __init__(self, pin_number):
        self.name = "LED"
        self.pin_number = pin_number
        self.status = False
        GPIO.setup(self.pin_number,GPIO.OUT)
        GPIO.output(self.pin_number,GPIO.LOW)

    def on(self):
        self.status = True
        GPIO.output(self.pin_number,GPIO.HIGH)

    def off(self):
        self.status = False
        GPIO.output(self.pin_number,GPIO.LOW)
