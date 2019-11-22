import time, math

from library_py.gps_py.Gps import Gps
from library_py.imu_py.Imu import Imu
from library_py.motors_py.Motors import Motors
from library_py.button_py.Button import Button


def searchTarget(latitude,longitude,latitudeTarget,longitudeTarget):
    relativePosition = { 'latitude':latitudeTarget - latitude,'longitude':longitudeTarget - longitude };
    angle_target = math.atan2(relativePosition['longitude'],relativePosition['latitude']);
    angle_target = angle_target*(180/math.pi);
    return  angle_target;

def distanceTarget(latitude,longitude,latitudeTarget,longitudeTarget):
    angoldist=math.sqrt(pow(latitudeTarget - latitude,2)+pow(longitudeTarget - longitude,2));
    return angoldist*6371000*math.pi/180;


def calibrate(angle_rover,correction):
    # signAngle = Math.sign(correction);
    if(correction>0):
        if(angle_rover<180-correction):
            return angle_rover + correction
        else:
            return angle_rover + correction -360;
    else:
        if(angle_rover>-180-correction):
            return angle_rover + correction
        else:
            return angle_rover + correction +360;
    return

def main():
    try:
        actuator_motor = Motors();
        gps_sensor = Gps();
        imu_sensor = Imu();
        gps_sensor.daemon = True;
        gps_sensor.start();
        imu_sensor.daemon = True;
        imu_sensor.start();

        button = Button(25);
        button.daemon = True;
        button.start();
        # actuator_motor.setForward();
        # da Aula 28 Spaccio
        # latitudeTarget = 41.89639;
        # longitudeTarget = 12.493626;
        # da Aula 28 Colosseo
        # latitudeTarget = 41.896467;
        # longitudeTarget = 12.492629;

        # da Aula 28 a Colle Oppio
        # latitudeTarget = 41.892606;
        # longitudeTarget = 12.495735;

        # da Aula 28 al Fauno
        latitudeTarget = 41.892887;
        longitudeTarget = 12.492930;

        # da Aula 28 a Colle Oppio
        # latitudeTarget = 41.893102;
        # longitudeTarget = 12.492427;

        # da Aula 28 a Colle Oppio
        # latitude get = 12.491561;

        # da Aula Uscita
        # latitudeTarget =41.892800;
        # longitudeTarget = 12.493178;

        # da Aula Entrata
        # latitudeTarget = 41.893136;
        # longitudeTarget = 12.494043;

        # 41.881979, 12.578023
        # latitudeTarget = 41.882013;
        # longitudeTarget = 12.578082;
        # 41.882013, 12.578082

        #Pozzo Chiostro
        # latitudeTarget = 41.893505;
        # longitudeTarget = 12.493300;



        # 41.893544, 12.493272

        # 41.894239, 12.496125

        #
        # latitudeTarget = 41.894239;
        # longitudeTarget = 12.496125;
        #
        # latitudeTarget = 41.893093;
        # longitudeTarget = 12.492153;

        # 41.893093, 12.492153

        k = 0;
        angle_target = 0;

        first_step = False;
        actuator_motor.setTurnLeft();
        # while(first_step == False):
        #     theta_bussola = imu_sensor.getDataFusion()['z'];
        #     # angle_rover = calibrate(angle_rover,0);
        #     # print(gps_sensor.getData()['longitude']);
        #     # print(gps_sensor.getData()['latitude']);
        #     theta_target = searchTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
        #     # angle_targetCoor = 90-angle_targetCoor;
        #     # angle_target = angle_targetCoor + angle_rover;
        #
        #     # print(angle_targetCoor);
        #     # print(angle_target);
        #     # actuator_motor.go(0,0);
        #     # time.sleep(0.05);
        #     # if(k < 254):
        #     #     k = k + 10;
        #     # else:
        #     #     k  = 0;
        #     # actuator_motor.setVelocity(200);
        #     # actuator_motor.setTurnLeft();
        #     delta_theta = theta_bussola - theta_target;
        #     print("theta_bussola:"+str(theta_bussola) );
        #     print("theta_target:"+str(theta_target) );
        #     print("delta_theta:"+str(delta_theta) );
        #     if(delta_theta < 10 and delta_theta > -10):
        #         first_step = True;
        #     else:
        #         actuator_motor.setRotation(150);



        actuator_motor.setForward();
        second_step = False;
        stop_motors = False;
        speed = 200;
        parameter=1;
        iter = 1;
        Longitudine = [];
        Latitudine = [];

        while(iter<5):
            Longitudine.append(gps_sensor.getData()['longitude']);
            Latitudine.append(gps_sensor.getData()['latitude']);
            time.sleep(1);
            iter=iter+1;
        Long_vera=sum(Longitudine)/(iter-1);
        Lat_vera=sum(Latitudine)/(iter-1);
        iter=1;
        while(second_step == False):

            theta_bussola = imu_sensor.getDataFusion()['z'];
            theta_target = searchTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
            distance_target = distanceTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
            if (iter==1):
                theta_target = searchTarget(Lat_vera,Long_vera,latitudeTarget,longitudeTarget);
                distance_target = distanceTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
            iter=2;
            print("distance:" + str(distance_target));
            delta_theta = (theta_bussola - theta_target);


            #print("theta_bussola:"+str(theta_bussola) );
            #print("theta_target:"+str(theta_target) );
            #print("delta_theta:"+str(delta_theta) );
            delta_theta = delta_theta *(math.pi/180);
            if(not button.status):
                if abs(delta_theta)>3.14/2:
                    parameter=-1;
                v1 = speed*(1+parameter*math.sin(delta_theta))
                v2 = speed*(1-parameter*math.sin(delta_theta))
                actuator_motor.go(int(v1),int(v2));
                stop_motors = False;
            else:
                if(not stop_motors):
                    actuator_motor.go(0,0);
                    stop_motors = True;

        actuator_motor.turnOff();
    except KeyboardInterrupt:
        actuator_motor.turnOff();

if __name__ == '__main__':
    main()
