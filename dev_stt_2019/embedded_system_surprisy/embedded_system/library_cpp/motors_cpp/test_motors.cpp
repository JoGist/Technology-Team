#include "Motors.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "Motors.cpp"
#include <unistd.h>


void ctrl_c_handler(int s){
  std::cout << "Caught signal " << s << std::endl;
  hat.resetAll();
  exit(1);
}


int main(int argc,char ** argv){
    Motors motor_actuator;
    signal(SIGINT, ctrl_c_handler);
    // motor_actuator.movement(1,180);
    // usleep(1000000);
    // motor_actuator.movement(2,180);
    // usleep(1000000);
    // motor_actuator.movement(3,180);
    // usleep(1000000);
    // motor_actuator.movement(4,180);
    // usleep(1000000);
    // motor_actuator.movement(5,180);
    // usleep(1000000);


    motor_actuator.go(140,200);
    usleep(2000000);

    // boolean loop=true;
    // int speed = 0;
    // while(speed<255){
    //     motor_actuator.go(speed,0);
    //     usleep(1000000);
    //     speed = speed + 10;
    // }
    motor_actuator.stop();
    hat.resetAll();
    return 0;
}
