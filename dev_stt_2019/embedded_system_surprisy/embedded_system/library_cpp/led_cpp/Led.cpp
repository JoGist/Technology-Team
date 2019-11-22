#include "Led.h"

using namespace std;

Led::Led(int pn,string c): pin_number(pn), color(c) {
    if(wiringPiSetupGpio() == -1) { //when initialize wiringPi failed, print message to screen
        printf("setup wiringPi failed !\n");
    }
}
void Led::on() {
    pinMode(pin_number, OUTPUT);
    digitalWrite(pin_number, HIGH);   //LED on
    // printf("LED  on\n");
}
void Led::off()
{
    pinMode(pin_number, OUTPUT);
    digitalWrite(pin_number, LOW);   //LED on
    // printf("LED  off\n");
}
