
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import time
import atexit
import multiprocessing

class Motors():
    def __init__(self):
        print("Loading Actuator...");
        self.mh = Adafruit_MotorHAT(addr=0x60)
        atexit.register(self.turnOffMotors)

        self.motor_left_front = self.mh.getMotor(3)
        self.motor_left_back = self.mh.getMotor(4)
        self.motor_right_back = self.mh.getMotor(1)
        self.motor_right_front = self.mh.getMotor(2)

        self.speed_motor_left_front = 0
        self.speed_motor_left_back = 0
        self.speed_motor_right_back = 0
        self.speed_motor_right_front = 0

        self.rotation_motor_left_front = 0
        self.rotation_motor_left_back = 0
        self.rotation_motor_right_back = 0
        self.rotation_motor_right_front = 0

        self.left_rotation = False;
        self.right_rotation = False;
        self.min = 100;

        # self.setForward();
        self.setForwardLeft(True);
        self.setForwardRight(True);
        print("Loaded Actuator...");

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

    def setForwardLeft(self,left_rotation):
        if(self.left_rotation != left_rotation):
            self.left_rotation = left_rotation;
            if(self.left_rotation == True):
                self.motor_left_front.run(Adafruit_MotorHAT.BACKWARD);
                self.motor_left_back.run(Adafruit_MotorHAT.FORWARD);
            else:
                self.motor_left_front.run(Adafruit_MotorHAT.FORWARD);
                self.motor_left_back.run(Adafruit_MotorHAT.BACKWARD);
    def setForwardRight(self,right_rotation):
        if(self.right_rotation != right_rotation):
            self.right_rotation = right_rotation;
            if(self.right_rotation == True):
                self.motor_right_back.run(Adafruit_MotorHAT.FORWARD);
                self.motor_right_front.run(Adafruit_MotorHAT.BACKWARD);
            else:
                self.motor_right_back.run(Adafruit_MotorHAT.BACKWARD);
                self.motor_right_front.run(Adafruit_MotorHAT.FORWARD);

    def setForward(self):
        self.motor_left_front.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_left_back.run(Adafruit_MotorHAT.FORWARD);
        self.motor_right_back.run(Adafruit_MotorHAT.FORWARD);
        self.motor_right_front.run(Adafruit_MotorHAT.BACKWARD);

        self.rotation_motor_left_front = -1
        self.rotation_motor_left_back = +1
        self.rotation_motor_right_back = +1
        self.rotation_motor_right_front = -1

    def setBackward(self):
        self.motor_left_front.run(Adafruit_MotorHAT.FORWARD);
        self.motor_left_back.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_right_back.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_right_front.run(Adafruit_MotorHAT.FORWARD);

        self.rotation_motor_left_front = +1
        self.rotation_motor_left_back = -1
        self.rotation_motor_right_back = -1
        self.rotation_motor_right_front = +1

    def setTurnLeft(self):
        self.motor_left_front.run(Adafruit_MotorHAT.FORWARD);
        self.motor_left_back.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_right_back.run(Adafruit_MotorHAT.FORWARD);
        self.motor_right_front.run(Adafruit_MotorHAT.BACKWARD);

        self.rotation_motor_left_front = -1
        self.rotation_motor_left_back = +1
        self.rotation_motor_right_back = -1
        self.rotation_motor_right_front = +1

    def setTurnRight(self):
        self.motor_left_front.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_left_back.run(Adafruit_MotorHAT.FORWARD);
        self.motor_right_back.run(Adafruit_MotorHAT.BACKWARD);
        self.motor_right_front.run(Adafruit_MotorHAT.FORWARD);

        self.rotation_motor_left_front = +1
        self.rotation_motor_left_back = -1
        self.rotation_motor_right_back = +1
        self.rotation_motor_right_front = -1

    def updateSpeedAllMotors(self):
        self.motor_left_front.setSpeed(self.speed_motor_left_front)
        self.motor_left_back.setSpeed(self.speed_motor_left_back)
        self.motor_right_back.setSpeed(self.speed_motor_right_back)
        self.motor_right_front.setSpeed(self.speed_motor_right_front)
    def setSpeedMotors(self,speed_motor_left_front,speed_motor_left_back,speed_motor_right_back,speed_motor_right_front):
        self.speed_motor_left_front = speed_motor_left_front
        self.speed_motor_left_back = speed_motor_left_back
        self.speed_motor_right_back = speed_motor_right_back
        self.speed_motor_right_front = speed_motor_right_front
    def getSpeedMotors(self):
        return [self.speed_motor_left_front,self.speed_motor_left_back,self.speed_motor_right_back,self.speed_motor_right_front]
    def getRotationsMotors(self):
        return [self.rotation_motor_left_front,self.rotation_motor_left_back,self.rotation_motor_right_back,self.rotation_motor_right_front]

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
    def go(self, v_left,v_right):
        rotation_left = True;
        rotation_right = True;
        if(v_left<0):
            rotation_left = False;
            v_left = abs(v_left);
        if(v_right<0):
            rotation_right = False;
            v_right = abs(v_right);
        self.setForwardLeft(rotation_left);
        self.setForwardRight(rotation_right);

        self.motor_left_back.setSpeed(v_left)
        self.motor_right_back.setSpeed(v_right)
        self.motor_right_front.setSpeed(v_right)
        self.motor_left_front.setSpeed(v_left)

    def stopMotors(self):
        self.motor_left_front.setSpeed(0)
        self.motor_left_back.setSpeed(0)
        self.motor_right_back.setSpeed(0)
        self.motor_right_front.setSpeed(0)

        self.speed_motor_left_front = 0
        self.speed_motor_left_back = 0
        self.speed_motor_right_back = 0
        self.speed_motor_right_front = 0
