#Encoder
import RPi.GPIO as GPIO                    #Import GPIO library
import time
import math
import threading
class Encoder(threading.Thread):
    def __init__(self,pinA,pinB):
        threading.Thread.__init__(self)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(pinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.pinA = pinA
        self.pinB = pinB
        self.radius = 3;
        self.distancePerRevolution = 2*math.pi*self.radius;
        self.pulsePerRevolution = 166;
        self.distancePerPulse = self.distancePerRevolution / self.pulsePerRevolution;
        self.countPulse = 0;
        self.status = True;
    def run(self):
        valuebefore = 1;
        valuenow = 1;
        start = (time.time()*1000) % 60
        while self.status:
            valuebefore = valuenow;
            if GPIO.input(self.pinA) == GPIO.LOW and GPIO.input(self.pinB) == GPIO.LOW:
                valuenow = 1;
            elif GPIO.input(self.pinA) == GPIO.LOW and GPIO.input(self.pinB) == GPIO.HIGH:
                valuenow = 2;
            elif GPIO.input(self.pinA) == GPIO.HIGH and GPIO.input(self.pinB) == GPIO.LOW:
                valuenow = 3;
            else:
                valuenow = 4;
            if valuenow != valuebefore:
                done = (time.time()*1000) % 60
                elapsed = (done - start)
                # print(elapsed)
                velocity = ((self.distancePerPulse) / elapsed);

                self.countPulse =self.countPulse +1;
                print(self.countPulse*self.distancePerPulse)
                # print(velocity)
                start = (time.time()*1000)% 60
