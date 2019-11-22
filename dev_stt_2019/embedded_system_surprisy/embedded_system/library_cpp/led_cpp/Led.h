#ifndef LED_H    // To make sure you don't declare the function more than once by including the header multiple times.
#define LED_H

#include <wiringPi.h>
#include <stdio.h>
#include <string>

using namespace std;

class Led {
 private:
     // string name;
     string color;
     int pin_number;
     bool status;

 public:
 Led(int n, string color);
 void setPinNumber(int pn);
 void on();
 void off();

};

#endif
