#DISTANCE_SENSOR
import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
import multiprocessing

class DistanceSensor():
    def __init__(self):
        self.distance = -1;
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering

        self.TRIG = 23                                  #Associate pin 23 to TRIG
        self.ECHO = 24                                  #Associate pin 24 to ECHO

        # print "Distance measurement in progress"

        GPIO.setup(self.TRIG,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(self.ECHO,GPIO.IN)                   #Set pin as GPIO in

    def uploadData(self):
        GPIO.output(self.TRIG, False)                 #Set TRIG as LOW
        # print "Waitng For Sensor To Settle"
        # time.sleep(0.0001)                            #Delay of 2 seconds

        GPIO.output(self.TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.01)                      #Delay of 0.00001 seconds
        GPIO.output(self.TRIG, False)                 #Set TRIG as LOW
        try:
            while GPIO.input(self.ECHO)==0:               #Check whether the ECHO is LOW
              pulse_start = time.time()
              pass             #Saves the last known time of LOW pulse
            while GPIO.input(self.ECHO)==1:               #Check whether the ECHO is HIGH
              pulse_end = time.time()               #Saves the last known time of HIGH pulse
              pass
              #Saves the last known time of HIGH pulse
              #print pulse_end

            pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

            distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
            distance = round(distance, 4)            #Round to two decimal points

            if distance > 2 and distance < 400:      #Check whether the distance is within range
                                                      # print "Distance:",distance - 0.5,"cm"
                                                      #Print distance with 0.5 cm calibration
              self.distance = distance-0.5;
            else:
              self.distance = -1
        except:
            print('Problem-distance-sensor')
            self.config_data()
            self.uploadData()
    def config_data(self):
        self.distance = -1;
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering

        self.TRIG = 23                                  #Associate pin 23 to TRIG
        self.ECHO = 24                                  #Associate pin 24 to ECHO

        # print "Distance measurement in progress"

        GPIO.setup(self.TRIG,GPIO.OUT)                  #Set pin as GPIO out
        GPIO.setup(self.ECHO,GPIO.IN)
    def getData(self):
        return self.distance

    def updateData(self):
        while True:
            self.uploadData()
            # print(self.getData()['gyro'])
            pass
    def auto_update(self):
        process = multiprocessing.Process(target=self.updateData, args=())
        process.daemon = True
        process.start()
