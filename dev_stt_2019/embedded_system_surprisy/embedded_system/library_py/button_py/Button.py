#Import Library
import RPi.GPIO as GPIO
import time
import threading

#naming convention
GPIO.setmode(GPIO.BCM)

#GPIO warning messages
GPIO.setwarnings(False)

class Button(threading.Thread):
    def __init__(self, pin_number):
        threading.Thread.__init__(self)
        self.pin_number = pin_number
        self.status = False;
        GPIO.setup(pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def run(self):
        while True:
            input_state = GPIO.input(self.pin_number)
            if input_state == False:
                self.status = not self.status
                time.sleep(0.2)
            time.sleep(0.01)
