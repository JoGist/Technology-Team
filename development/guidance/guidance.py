import curses
#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
motor1 = mh.getMotor(1)
motor2 = mh.getMotor(2)
motor3 = mh.getMotor(3)
motor4 = mh.getMotor(4)

k=240
flag = False

def setForward():
    motor1.run(Adafruit_MotorHAT.BACKWARD);
    motor2.run(Adafruit_MotorHAT.FORWARD);
    motor3.run(Adafruit_MotorHAT.FORWARD);
    motor4.run(Adafruit_MotorHAT.BACKWARD);

def setBackward():
    motor1.run(Adafruit_MotorHAT.FORWARD);
    motor2.run(Adafruit_MotorHAT.BACKWARD);
    motor3.run(Adafruit_MotorHAT.BACKWARD);
    motor4.run(Adafruit_MotorHAT.FORWARD);

def setTurnLeft():
   motor1.run(Adafruit_MotorHAT.BACKWARD);
   motor2.run(Adafruit_MotorHAT.FORWARD);
   motor3.run(Adafruit_MotorHAT.BACKWARD);
   motor4.run(Adafruit_MotorHAT.FORWARD);

def setTurnRight():
	motor1.run(Adafruit_MotorHAT.FORWARD);
	motor2.run(Adafruit_MotorHAT.BACKWARD);
	motor3.run(Adafruit_MotorHAT.FORWARD);
	motor4.run(Adafruit_MotorHAT.BACKWARD);
#
# def setSpeedMotors(m1,m2,m3,m4):
def setSpeed(speed,speedLeft, speedRight):
    if speed >= 0:
        setForward();
    else:
        setBackward();
        speed = -speed;
    motor1.setSpeed(speed+speedLeft);
    motor2.setSpeed(speed+speedLeft);

    motor3.setSpeed(speed+speedRight);
    motor4.setSpeed(speed+speedRight);

def main(win):
    atexit.register(turnOffMotors)

    ################################# DC motor test!
    motor1 = mh.getMotor(1)
    motor2 = mh.getMotor(2)
    motor3 = mh.getMotor(3)
    motor4 = mh.getMotor(4)

    # set the speed to start, from 0 (off) to 255 (max speed)

    # win.nodelay(True)
    key=""
    # win.clear()
    # win.addstr("Detected key:")
    i=0;
    speed = 0;
    speedLeft = 0;
    speedRight = 0;
    speedRotationInit = 40;
    speedRotation = speedRotationInit;
    while 1:
        try:
           key = win.getkey()
           win.clear()
           print str(key + '\n')
           if key == 'KEY_UP':
              speedLeft = 0;
              speedRight = 0;
              speedRotation = speed;
              if speed<k:
                  speed = speed + 15;
                  setSpeed(speed,0,0);
              win.addstr("Detected key:")
              win.addstr(str(key))
              print str(key + '\n' + speed)
           if key == 'KEY_DOWN':
              speedLeft = 0;
              speedRight = 0;
              speedRotation = speed;
              setBackward();
              if speed>-k:
                  speed = speed - 15;
                  setSpeed(speed,0,0);
              win.addstr("Detected key:")
              win.addstr(str(key))
              print str(key + '\n')
           if key == 'KEY_LEFT':
              speedLeft = 0;
              speedRight = 0;
              setTurnLeft();
              if speedRotation<k:
				speedRotation = speedRotation + 5
				motor1.setSpeed(speedRotation);
				motor2.setSpeed(speedRotation);
				motor3.setSpeed(speedRotation);
				motor4.setSpeed(speedRotation);
				win.addstr("Detected key:")
				win.addstr(str(speedRotation))
				print str(speedRotation + '\n')
           if key == 'KEY_RIGHT':
              setTurnRight();
              speedLeft = 0;
              speedRight = 0;
              if speedRotation<k:
				speedRotation = speedRotation + 5
				motor1.setSpeed(speedRotation);
				motor2.setSpeed(speedRotation);
				motor3.setSpeed(speedRotation);
				motor4.setSpeed(speedRotation);
				win.addstr("Detected key:\n")
				win.addstr(str(key))
				win.addstr("Speed Rotation:")
				win.addstr(str(speedRotation))
           if key == 'q':
	           speedRotation = speedRotationInit;
	           speedLeft = speedLeft + 3;
	           if speed+speedLeft<k:
	               setSpeed(speed,speedLeft, 0)
	               win.addstr("Detected key:")
	               win.addstr(str(key))
	               print str(key + '\n')
           if key == 'e':
	           speedRotation = speedRotationInit;
	           speedRight = speedRight + 3;
	           if speed+speedRight<k:
	               setSpeed(speed,0,speedRight)
	               win.addstr("Detected key:")
	               win.addstr(str(key))
	               print str(key + '\n')
           if key == 's':
              speedLeft = 0;
              speedRight = 0;
              speedRotation = speedRotationInit;
              speed = 0;
              setSpeed(0,0,0);
           if key == 'd':
               motor1.run(Adafruit_MotorHAT.BACKWARD);
               motor2.run(Adafruit_MotorHAT.FORWARD);
               motor3.run(Adafruit_MotorHAT.FORWARD);
               motor4.run(Adafruit_MotorHAT.BACKWARD);
               if i<k:
                   motor1.setSpeed(i+140);
                   motor2.setSpeed(i+140);
                   motor3.setSpeed(i);
                   motor4.setSpeed(i);
                   i = i + 20;
               win.addstr("Detected key:")
               win.addstr(str(key))

           if key == os.linesep:
              break
        except Exception as e:
           # No input
           pass

curses.wrapper(main)
