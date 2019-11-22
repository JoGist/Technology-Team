#ifndef GPS_H    // To make sure you don't declare the function more than once by including the header multiple times.
#define GPS_H

#include <wiringPi.h>
#include <wiringSerial.h>
#include <string.h>
#include <iostream>

//
using namespace std;

class Gps {
 private:

     int serial_port;
     bool status;
     char dat;

 public:
     double longitude=500;
     double latitude=500;
     Gps();
     void updateData();
     double getLatitude();
     double getLongitude();
     bool getStatus();

};

#endif
