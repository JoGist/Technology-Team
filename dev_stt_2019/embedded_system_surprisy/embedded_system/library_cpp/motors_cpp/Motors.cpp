#include "Motors.h"
// #include <wiringPi.h>
// #include <stdio.h>
// #include <string.h>
// #include <iostream>

// #include "stdio.h"
// #include <iostream>
// #include <signal.h>
// #include <unistd.h>
// //
// using namespace std;

// Motor::Motor() {
//     // signal(SIGINT, ctrl_c_handler);
//     myMotor = hat.getDC(1);
// }

Motors::Motors() : ledVerde(4,"Verde"),ledGiallo(13,"Giallo"),ledBlu(17,"Blu"),ledRosso(18,"Rosso"){ //Uninitialized reference member

 }
bool Motors::getSpeed() {
    return speed;
}

void Motors::avanti(int speed) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.setSpeed(speed);
    myMotor2.setSpeed(speed);
    myMotor3.setSpeed(speed);
    myMotor4.setSpeed(speed);
    myMotor1.run(BACKWARD);
    myMotor2.run(FORWARD);
    myMotor3.run(FORWARD);
    myMotor4.run(BACKWARD);
    ledRosso.off();
    ledGiallo.off();
    ledVerde.on();
    ledBlu.off();
}

void Motors::go(int speedDestra, int speedSinistra) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.setSpeed(speedDestra);
    myMotor2.setSpeed(speedDestra);
    myMotor3.setSpeed(speedSinistra);
    myMotor4.setSpeed(speedSinistra);
    myMotor1.run(BACKWARD);
    myMotor2.run(FORWARD);
    myMotor3.run(FORWARD);
    myMotor4.run(BACKWARD);
    ledRosso.off();
    ledGiallo.off();
    ledVerde.on();
    ledBlu.off();
}

// void Motor::avanti(int speed) {
//     // set the speed to start, from 0 (off) to 255 (max speed)
//     myMotor1.setSpeed(speed);
//     myMotor2.setSpeed(speed);
//     myMotor3.setSpeed(speed);
//     myMotor4.setSpeed(speed);
//     myMotor1.run(BACKWARD);
//     myMotor2.run(FORWARD);
//     myMotor3.run(FORWARD);
//     myMotor4.run(BACKWARD);
//     ledRosso.off();
//     ledGiallo.off();
//     ledVerde.on();
//     ledBlu.off();
// }

void Motors::indietro(int speed) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.setSpeed(speed);
    myMotor2.setSpeed(speed);
    myMotor3.setSpeed(speed);
    myMotor4.setSpeed(speed);
    myMotor1.run(FORWARD);
    myMotor2.run(BACKWARD);
    myMotor3.run(BACKWARD);
    myMotor4.run(FORWARD);
    ledRosso.off();
    ledGiallo.off();
    ledVerde.off();
    ledBlu.on();
}

void Motors::giroOrario(int speed) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.setSpeed(speed);
    myMotor2.setSpeed(speed);
    myMotor3.setSpeed(speed);
    myMotor4.setSpeed(speed);
    myMotor1.run(FORWARD);
    myMotor2.run(BACKWARD);
    myMotor3.run(FORWARD);
    myMotor4.run(BACKWARD);
    ledRosso.on();
    ledGiallo.off();
    ledVerde.off();
    ledBlu.off();

}
void Motors::giroAntiorario(int speed) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.setSpeed(speed);
    myMotor2.setSpeed(speed);
    myMotor3.setSpeed(speed);
    myMotor4.setSpeed(speed);
    myMotor1.run(BACKWARD);
    myMotor2.run(FORWARD);
    myMotor3.run(BACKWARD);
    myMotor4.run(FORWARD);
    ledRosso.off();
    ledGiallo.on();
    ledVerde.off();
    ledBlu.off();
}
void Motors::stop() {
    // set the speed to start, from 0 (off) to 255 (max speed)
    myMotor1.run(RELEASE);
    myMotor2.run(RELEASE);
    myMotor3.run(RELEASE);
    myMotor4.run(RELEASE);
    ledRosso.off();
    ledGiallo.off();
    ledVerde.off();
    ledBlu.off();
}
void Motors::movement(int movementCode,int speed) {
    // set the speed to start, from 0 (off) to 255 (max speed)
    if (movementCode == 1){
        this->avanti(speed);
    } else if(movementCode == 2){
        this->indietro(speed);
    } else if(movementCode == 3){
        this->giroOrario(speed);
    } else if(movementCode == 4){
        this->giroAntiorario(speed);
    } else{
        this->stop();
    }
}
//
void Motors::ctrl_c_handler(int s){
    std::cout << "Caught signal " << s << std::endl;
    hat.resetAll();
    exit(1);
}
