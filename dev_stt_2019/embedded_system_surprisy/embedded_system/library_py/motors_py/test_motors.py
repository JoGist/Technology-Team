import time, math

from Motors import Motors

def main():
    try:
        print("Start Test Motors");
        actuator_motor = Motors();
        # actuator_motor.turnOff();
        speed = 0;
        speedMax = 200;
        add = 10;
        parameter = 1;

        # k = 0;
        # while(True):
        #     print(speed);
        #     if(speed > speedMax):
        #         parameter = -1;
        #         actuator_motor.setForward();
        #     elif(speed < 0):
        #         parameter = 1;
        #         actuator_motor.setBackward();
        #     time.sleep(0.1);
        #     if(parameter == 1):
        #         speed = speed + add;
        #     else:
        #         speed = speed - add;
        #     actuator_motor.go(speed-40,speed);
        #     k = k + 1;
        speed = 255;
        while(True):
            # print(speed);
            actuator_motor.go(-130,speed);
            # k = k + 1;

    except KeyboardInterrupt:
            actuator_motor.turnOff();

if __name__ == '__main__':
    main()
