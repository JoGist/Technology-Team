
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import multiprocessing
import time


class Motors():
    def __init__(self):
        self.mh = Adafruit_MotorHAT(addr=0x60)
        atexit.register(self.turnOffMotors)

        self.motor1 = self.mh.getMotor(1)
        self.motor2 = self.mh.getMotor(2)
        self.motor3 = self.mh.getMotor(3)
        self.motor4 = self.mh.getMotor(4)

        self.speed_m1 = 0
        self.speed_m2 = 0
        self.speed_m3 = 0
        self.speed_m4 = 0

        self.rotation_m1 = 0
        self.rotation_m2 = 0
        self.rotation_m3 = 0
        self.rotation_m4 = 0

        self.setForward();

    def turnOffMotors(self):
    	self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    def turnOff(self):
        atexit.register(self.turnOffMotors)
    	self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    	self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)
    def setForward(self):
        self.motor1.run(Adafruit_MotorHAT.BACKWARD);
        self.motor2.run(Adafruit_MotorHAT.FORWARD);
        self.motor3.run(Adafruit_MotorHAT.FORWARD);
        self.motor4.run(Adafruit_MotorHAT.BACKWARD);

        self.rotation_m1 = -1
        self.rotation_m2 = +1
        self.rotation_m3 = +1
        self.rotation_m4 = -1

    def setBackward(self):
        self.motor1.run(Adafruit_MotorHAT.FORWARD);
        self.motor2.run(Adafruit_MotorHAT.BACKWARD);
        self.motor3.run(Adafruit_MotorHAT.BACKWARD);
        self.motor4.run(Adafruit_MotorHAT.FORWARD);

        self.rotation_m1 = +1
        self.rotation_m2 = -1
        self.rotation_m3 = -1
        self.rotation_m4 = +1

    def setTurnLeft(self):
        self.motor1.run(Adafruit_MotorHAT.BACKWARD);
        self.motor2.run(Adafruit_MotorHAT.FORWARD);
        self.motor3.run(Adafruit_MotorHAT.BACKWARD);
        self.motor4.run(Adafruit_MotorHAT.FORWARD);

        self.rotation_m1 = -1
        self.rotation_m2 = +1
        self.rotation_m3 = -1
        self.rotation_m4 = +1

    def setTurnRight(self):
        self.motor1.run(Adafruit_MotorHAT.FORWARD);
        self.motor2.run(Adafruit_MotorHAT.BACKWARD);
        self.motor3.run(Adafruit_MotorHAT.FORWARD);
        self.motor4.run(Adafruit_MotorHAT.BACKWARD);

        self.rotation_m1 = +1
        self.rotation_m2 = -1
        self.rotation_m3 = +1
        self.rotation_m4 = -1

    def updateSpeedAllMotors(self):
        self.motor1.setSpeed(self.speed_m1)
        self.motor2.setSpeed(self.speed_m2)
        self.motor3.setSpeed(self.speed_m3)
        self.motor4.setSpeed(self.speed_m4)

    def setSpeedMotors(self,speed_m1,speed_m2,speed_m3,speed_m4):
        self.speed_m1 = speed_m1
        self.speed_m2 = speed_m2
        self.speed_m3 = speed_m3
        self.speed_m4 = speed_m4

    def getSpeedMotors(self):
        return [self.speed_m1,self.speed_m2,self.speed_m3,self.speed_m4]

    def getRotationsMotors(self):
        return [self.rotation_m1,self.rotation_m2,self.rotation_m3,self.rotation_m4]

    def setVelocity(self, velocity):
        if velocity >= 0:
            self.setForward();
            speed = velocity;
        else:
            self.setBackward();
            speed = -velocity;
        self.setSpeedMotors(speed,speed,speed,speed)
        self.updateSpeedAllMotors()

    def setRotation(self, angular_velocity):
        if angular_velocity >= 0:
            self.setTurnLeft();
            speed = angular_velocity;
        else:
            self.setTurnRight();
            speed = -angular_velocity;
        self.setSpeedMotors(speed,speed,speed,speed)
        self.updateSpeedAllMotors()
        
    def stopMotors(self):
        self.motor1.setSpeed(0)
        self.motor2.setSpeed(0)
        self.motor3.setSpeed(0)
        self.motor4.setSpeed(0)

        self.speed_m1 = 0
        self.speed_m2 = 0
        self.speed_m3 = 0
        self.speed_m4 = 0
