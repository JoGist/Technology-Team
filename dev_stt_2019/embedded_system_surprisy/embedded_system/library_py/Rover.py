import time, json, math, csv
import threading

from gps_py.Gps import Gps
from imu_py.Imu import Imu
from battery_py.Battery import Battery
from motors_py.Motors import Motors
from button_py.Button import Button
from communication_py.Socket import Socket
from communication_py.SocketUDP import SocketUDP
from communication_py.Antenna import Antenna

millis = lambda: int(round(time.time() * 1000))

class Rover(threading.Thread):
    def __init__(self,name="Surprice",coordinatesTarget = {'latitude':41.881410,'longitude':12.578107}):
        threading.Thread.__init__(self)
        print("Loading Rover System...");
        self.name = name;
        self.status = 0;

        self.STATUS_WAITING = 0;
        self.STATUS_WAIT_FOR_DEPLOYMENT = 1;
        self.STATUS_DEPLOYMENT_AND_FALL = 2;
        self.STATUS_LANDING = 3;
        self.STATUS_GO_TO_THE_TARGET = 4;
        self.STATUS_REACHED_TARGET = 5;
        self.ABORT_MISSION = 10;

        self.coordinatesTarget = coordinatesTarget;
        self.pressureGround = self.readPressureGround();

        self.fusionPose = {'roll':0,'pitch':0,'theta_bussola':0}
        self.accel = {'ax':0,'ay':0,'az':0}
        self.gyro = {'x':0,'y':0,'z':0}

        self.pressure = 1.;
        self.temperature = 0.;

        self.coordinates = {};

        self.altitude = 1.;
        self.theta_target = 0;
        self.distance_target = 0;

        self.speed = 200;
        self.v_left = 0;
        self.v_right = 0;
        self.parameter = 1;

        self.t = 0;
        self.time_intervals = [0,0,0,0,0,0];
        self.time_landing = 5000;
        self.start_mission = False;
        self.abort_mission = False;

        #Loading Motors
        self.actuator_motor = Motors();

        #Loading Gps Sensor
        self.gps_sensor = Gps();
        self.coordinates = self.gps_sensor.getData();
        self.gps_sensor.daemon = True;
        self.gps_sensor.start();#Update Gps Data

        #Loading Imu Sensor
        self.imu_sensor = Imu(name);
        self.imu_sensor.daemon = True;
        self.imu_sensor.start();#Update Imu Data

        self.antenna = Antenna();
        self.antenna.daemon = True;
        self.antenna.start();
        print("Loaded Rover System...");

    def run(self):
        self.start_time = millis();
        while(True):
            while(self.status != self.ABORT_MISSION):
                self.now = millis();
                self.t = self.now - self.start_time;
                self.updateEssentialData();
                self.preparePackagesForSending();
                if(self.status == self.STATUS_WAITING):
                    self.time_intervals[0] = self.t;
                elif(self.status == self.STATUS_WAIT_FOR_DEPLOYMENT):
                    if(self.t-self.time_intervals[0]>2000):
                        print("Deployment and fall");
                        self.status = 2;
                        self.time_intervals[1] = self.t;
                elif(self.status == self.STATUS_DEPLOYMENT_AND_FALL):
                    if(self.t-self.time_intervals[1]>2000):
                        self.status = 3;
                        print("Landing");
                        self.time_intervals[2] = self.t;
                elif(self.status == self.STATUS_LANDING):
                    if(self.t-self.time_intervals[2]>1000):
                        self.status = 4;
                        print("Go to the target");
                        self.time_intervals[3] = self.t;
                elif(self.status == self.STATUS_GO_TO_THE_TARGET):
                    delta_theta = (self.fusionPose['theta_bussola'] - self.theta_target);
                    delta_theta = delta_theta *(math.pi/180);
                    if math.cos(delta_theta)<0:
                        self.parameter=-1;
                    self.v_left = self.speed*(1+self.parameter*math.sin(delta_theta))
                    self.v_right = self.speed*(1-self.parameter*math.sin(delta_theta))
                    # print(self.v_left,self.v_right);
                    self.actuator_motor.go(int(self.v_left),int(self.v_right));
                elif(self.status == self.STATUS_REACHED_TARGET):
                    # print("Status 5");
                    self.status = 6;
                    self.time_intervals[5] = self.t;
                time.sleep(0.01);

            self.updateEssentialData();
            self.preparePackagesForSending();
            time.sleep(0.01);

    # START TOOLS FOR TARGET
    def searchTarget(self,latitude,longitude,latitudeTarget,longitudeTarget):
        relativePosition = { 'latitude':latitudeTarget - latitude,'longitude':longitudeTarget - longitude };
        angle_target = math.atan2(relativePosition['longitude'],relativePosition['latitude']);
        angle_target = angle_target*(180/math.pi);
        return  angle_target;

    def distanceTarget(self,latitude,longitude,latitudeTarget,longitudeTarget):
        angoldist=math.sqrt(pow(latitudeTarget - latitude,2)+pow(longitudeTarget - longitude,2));
        return angoldist*6371000*math.pi/180;

    def getComputeAltitude(self):
        g=9.81;
        R=287;
        T0=290;
        P=self.pressure;
        if(self.pressure == 0):
            P = 1.
        return (-(R*T0)/g)*math.log(P/self.pressureGround);

    def computeHeight(self):
        return 44330.8 * (1 - pow(self.pressure / self.pressureGround, 0.190263));
    # END TOOLS FOR TARGET

    # START TOOLS FOR COMMUNICATION
    def updateEssentialData(self):
        self.theta_target = self.searchTarget(self.coordinates['latitude'],self.coordinates['longitude'],self.coordinatesTarget['latitude'],self.coordinatesTarget['longitude']);
        self.distance_target = self.distanceTarget(self.coordinates['latitude'],self.coordinates['longitude'],self.coordinatesTarget['latitude'],self.coordinatesTarget['longitude']);
        if(self.imu_sensor.status):
            self.fusionPose['roll'] = self.imu_sensor.data['fusionPose'][0]*(180/3.141);
            self.fusionPose['pitch'] = self.imu_sensor.data['fusionPose'][1]*(180/3.141);
            self.fusionPose['theta_bussola'] = self.imu_sensor.data['fusionPose'][2]*(180/3.141);

            self.pressure = self.imu_sensor.data["pressure"];
            self.temeprature = self.imu_sensor.data["temperature"];

            self.accel['ax'] = self.imu_sensor.data['accel'][0];
            self.accel['ay'] = self.imu_sensor.data['accel'][1];
            self.accel['az'] = self.imu_sensor.data['accel'][2];

            self.gyro['x'] = self.imu_sensor.data['gyro'][0];
            self.gyro['y'] = self.imu_sensor.data['gyro'][1];
            self.gyro['z'] = self.imu_sensor.data['gyro'][2];

            self.altitude = self.getComputeAltitude();
        if(self.gps_sensor.status):
            self.coordinates = self.gps_sensor.getData();
        if(self.antenna.dataMessageReceived == "0"):
            self.status = self.STATUS_WAITING;
            self.start_mission = False;
        if(self.antenna.dataMessageReceived == "1" and self.start_mission == False):
            self.status = self.STATUS_WAIT_FOR_DEPLOYMENT;
            self.start_mission = True;
            # self.start_time = millis();
            # self.time_intervals[0] = self.t
        if(self.antenna.dataMessageReceived == "10" and self.start_mission == True):
            self.status = self.ABORT_MISSION;
            self.abort_mission = True;
            self.start_mission = False;
            self.actuator_motor.turnOffMotors();

    def preparePackagesForSending(self):
        self.antenna.updateDataMessage1(self.getPackageMessageData1());
        self.antenna.updateDataMessage2(self.getPackageMessageData2());
        self.antenna.updateDataMessage3(self.getPackageMessageData3());
        self.antenna.updateDataMessage4(self.getPackageMessageData4());
        self.antenna.updateDataMessage5(self.getPackageMessageData5());
        self.antenna.updateDataMessage6(self.getPackageMessageData6());

    def getPackageMessageData1(self):
        delimiter = ";";
        status_str = str(self.status);
        theta_bussola_str =  str(round(self.fusionPose['theta_bussola'], 4));
        roll_str =  str(round(self.fusionPose['roll'], 4));
        pitch_str =  str(round(self.fusionPose['pitch'], 4));
        return "1" + delimiter + status_str + delimiter + theta_bussola_str + delimiter + roll_str + delimiter + pitch_str;
    def getPackageMessageData2(self):
        delimiter = ";";
        status_str = str(self.status);
        latitude = str(round(self.coordinates['latitude'],6));
        longitude = str(round(self.coordinates['longitude'],6));
        altitude_str = str(round(self.altitude, 4));
        return "2" + delimiter + status_str + delimiter + latitude + delimiter + longitude + delimiter + altitude_str;
    def getPackageMessageData3(self):
        delimiter = ";";
        status_str = str(self.status);
        theta_target_str = str(round(self.theta_target, 4));
        distance_target_str = str(round(self.distance_target, 4));
        time_str = str(round(self.t, 4));
        return "3" + delimiter + status_str + delimiter + theta_target_str + delimiter + distance_target_str + delimiter + time_str;
    def getPackageMessageData4(self):
        delimiter = ";";
        status_str = str(self.status);
        v_left_str = str(round(self.v_left, 1));
        v_right_str = str(round(self.v_right, 1));
        return "4" + delimiter + status_str + delimiter + v_left_str + delimiter + v_right_str;
    def getPackageMessageData5(self):
        delimiter = ";";
        status_str = str(self.status);
        accel_ax = str(round(self.accel['ax'], 5));
        accel_ay = str(round(self.accel['ay'], 5));
        accel_az = str(round(self.accel['az'], 5));
        return "5" + delimiter + status_str + delimiter + accel_ax + delimiter + accel_ay + delimiter + accel_az;
    def getPackageMessageData6(self):
        delimiter = ";";
        status_str = str(self.status);
        gyro_x = str(round(self.gyro['x'], 5));
        gyro_y = str(round(self.gyro['y'], 5));
        gyro_z = str(round(self.gyro['z'], 5));
        return "6" + delimiter + status_str + delimiter + gyro_x + delimiter + gyro_y + delimiter + gyro_z;
    # END TOOLS FOR COMMUNICATION

    # START TOOLS FOR SETTINGS
    def readPressureGround(self):
        file = "settings/pressure_ground.csv"
        try:
            with open(file) as csv_file:
                # csv_reader = csv.reader(csv_file, delimiter=',')
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    return float(row['pressure']);
        except:
            print("Problem load ground pressure");
            return 1013.30;
    # END TOOLS FOR SETTINGS

    # START FUNCTIONS FOR READ DATA
    def getHeaderData(self):
        return ["time","status","roll","pitch","theta_bussola","latitude","longitude","altitude","theta_target","distance_target","v_left","v_right","accel_x","accel_y","accel_z","gyro_x","gyro_y","gyro_z"];
    def getData(self):
        return {'time':self.t,"status":self.status,
                'roll':round(self.fusionPose['roll'],4),'pitch':round(self.fusionPose['pitch'],4),'theta_bussola':round(self.fusionPose['theta_bussola'],4),
                'latitude':round(self.coordinates['latitude'],4),'longitude':round(self.coordinates['longitude'],4),
                'altitude':round(self.altitude,4),
                'theta_target':round(self.theta_target,4),'distance_target':round(self.distance_target,4),
                'v_left':round(self.v_left,4),'v_right':round(self.v_right,4),
                'accel_x':round(self.accel['ax'],5),'accel_y':round(self.accel['ay'],5),'accel_z':round(self.accel['az'],5),
                'gyro_x':round(self.gyro['x'],5),'gyro_y':round(self.gyro['y'],5),'gyro_z':round(self.gyro['z'],5)};

    # END FUNCTIONS FOR READ DATA


            # 41.894056, 12.494044    1)
            # 41.892650, 12.493427    2)
            # 41.893296, 12.495741    3)
            # 41.892853, 12.492811    4)
