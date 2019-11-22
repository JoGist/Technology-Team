#ifndef MOTORS_H    // To make sure you don't declare the function more than once by including the header multiple times.
#define MOTORS_H

// PWM.cpp Adafruit_MotorHAT.cpp DCMotorTest.cpp
#include "AdafruitStepperMotorHAT_CPP/Adafruit_MotorHAT.h"
#include "AdafruitStepperMotorHAT_CPP/Adafruit_MotorHAT.cpp"
#include "AdafruitStepperMotorHAT_CPP/PWM.h"
#include "AdafruitStepperMotorHAT_CPP/PWM.cpp"
#include "stdio.h"
#include <iostream>
#include <signal.h>
#include <unistd.h>
#include "../led_cpp/Led.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "../led_cpp/Led.cpp"

//
using namespace std;
Adafruit_MotorHAT hat;
// Led l1(4,"Verde");
// Led l2(13,"Giallo");
// Led l3(17,"Blu");
// Led l4(18,"Rosso");
class Motors {
 private:
     Adafruit_DCMotor& myMotor1 = hat.getDC(1);
     Adafruit_DCMotor& myMotor2 = hat.getDC(2);
     Adafruit_DCMotor& myMotor3 = hat.getDC(3);
     Adafruit_DCMotor& myMotor4 = hat.getDC(4);
     Led ledVerde;
     Led ledGiallo;
     Led ledBlu;
     Led ledRosso;
     bool status;
     int speed;
 public:
     Motors();
     void ctrl_c_handler(int s);
     void avanti(int speed);
     void go(int speedDestra, int speedSinistra);
     void indietro(int speed);
     void giroOrario(int speed);
     void giroAntiorario(int speed);
     void giro(int speed);
     void stop();
     void movement(int movementCode,int speed);
     bool getSpeed();
};

#endif
