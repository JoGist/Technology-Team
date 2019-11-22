import Adafruit_PCA9685

class Pantilt():
    def __init__(self):
        self.sg = 0
        self.sd = 0
        #self.zero1 = 450
        #self.zero2 = 340
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)

    def setOrientation(self, x, y):
        #print(str(x)+" "+str(y))
        sg = int(375 - x*2.3)
        sd = int(450 - y*2.8)
        #print(str(sd)+" "+str(sg))
        self.pwm.set_pwm(0, 0, sd)
        self.pwm.set_pwm(1, 0, sg)
