import time, json, math

from library_py.gps_py.Gps import Gps
from library_py.imu_py.Imu import Imu
from library_py.battery_py.Battery import Battery
from library_py.motors_py.Motors import Motors
from library_py.button_py.Button import Button
from library_py.communication_py.Socket import Socket
from library_py.communication_py.SocketUDP import SocketUDP
from library_py.communication_py.Antenna import Antenna


def searchTarget(latitude,longitude,latitudeTarget,longitudeTarget):
    relativePosition = { 'latitude':latitudeTarget - latitude,'longitude':longitudeTarget - longitude };
    angle_target = math.atan2(relativePosition['longitude'],relativePosition['latitude']);
    angle_target = angle_target*(180/math.pi);
    return  angle_target;

def distanceTarget(latitude,longitude,latitudeTarget,longitudeTarget):
    angoldist=math.sqrt(pow(latitudeTarget - latitude,2)+pow(longitudeTarget - longitude,2));
    return angoldist*6371000*math.pi/180;
def main():
    delimiter = ";"
    try:
        print("Loading System");
        actuator_motor = Motors();
        gps_sensor = Gps();
        gps_sensor.daemon = True;
        gps_sensor.start();

        imu_sensor = Imu();
        imu_sensor.daemon = True;
        imu_sensor.start();

        button = Button(25);
        button.daemon = True;
        button.start();

        # socket = Socket();
        # socket.daemon = True;
        # socket.start();
        #
        # socketUDP = SocketUDP("172.20.10.3");
        socketUDP = SocketUDP("192.168.1.119");
        socketUDP.daemon = True;
        socketUDP.start();

        antenna = Antenna();
        antenna.daemon = True;
        antenna.start();

        battery = Battery();
        battery.daemon = True;
        battery.start();

        pressureZero =  1015.75

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

        print("Start Guidance System");

        # actuator_motor.setForward();
        second_step = False;
        stop_motors = False;
        speed = 200;
        parameter=1;
        iter = 1;
        Longitudine = [];
        Latitudine = [];
        print(imu_sensor.getPressure());
        time.sleep(0.1);
        data_updated = imu_sensor.getData();
        data_updated['gps'] = gps_sensor.getData();
        data_updated['altitude'] = imu_sensor.getAltitude(pressureZero);
        data_updated['voltage'] = battery.getVoltage();
        jsonarray = json.dumps(data_updated);
        # socketUDP.sendMessage(jsonarray);
        time.sleep(1);
        while(socketUDP.task != 10):
            if(socketUDP.task == 1):
                time.sleep(0.1);
                data_updated = imu_sensor.getData();
                data_updated['gps'] = gps_sensor.getData();
                data_updated['altitude'] = imu_sensor.getAltitude(pressureZero);
                data_updated['voltage'] = battery.getVoltage();
                jsonarray = json.dumps(data_updated);
                # socketUDP.sendMessage(jsonarray);
                theta_bussola = imu_sensor.getDataFusion()['z'];

                data = str(round(theta_bussola, 2))+delimiter+str(round(data_updated['altitude'], 2))+delimiter+str(round(data_updated['gps']['latitude'],4))+delimiter+str(round(data_updated['gps']['longitude'],4))
                antenna.sendMessage(data);
                # print(jsonarray);
                # socket.sendMessage('data_sensors',jsonarray);

                # print(imu_sensor.getPressure());
                while(imu_sensor.getAltitude(pressureZero) < 1 and imu_sensor.getAltitude(pressureZero) > -1):
                # while(True):
                    while(iter<5):
                        Longitudine.append(gps_sensor.getData()['longitude']);
                        Latitudine.append(gps_sensor.getData()['latitude']);
                        time.sleep(1);
                        iter=iter+1;
                    Long_vera=sum(Longitudine)/(iter-1);
                    Lat_vera=sum(Latitudine)/(iter-1);
                    iter=1;
                    while(second_step == False):
                        data_updated = imu_sensor.getData();
                        data_updated['gps'] = gps_sensor.getData();
                        data_updated['altitude'] = imu_sensor.getAltitude(pressureZero);
                        data_updated['voltage'] = battery.getVoltage();
                        jsonarray = json.dumps(data_updated);
                        # print(jsonarray);
                        # socket.sendMessage('data_sensors',jsonarray);
                        # s = socketUDP.sendMessage(jsonarray);
                        theta_bussola = imu_sensor.getDataFusion()['z'];
                        antenna.sendMessage(theta_bussola);
                        theta_target = searchTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
                        distance_target = distanceTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
                        if (iter==1):
                            theta_target = searchTarget(Lat_vera,Long_vera,latitudeTarget,longitudeTarget);
                            distance_target = distanceTarget(gps_sensor.getData()['latitude'],gps_sensor.getData()['longitude'],latitudeTarget,longitudeTarget);
                        iter=2;
                        # print("distance:" + str(distance_target));
                        delta_theta = (theta_bussola - theta_target);

                        # print("theta_bussola:"+str(theta_bussola) );
                        # print("theta_target:"+str(theta_target) );
                        # print("delta_theta:"+str(delta_theta) );
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
