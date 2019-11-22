# import sys
# sys.path.append('.')
import RTIMU, json, time, math
import threading

class Imu(threading.Thread):
    def __init__(self,code="Surprice"):
        print("Loading Imu Sensor...");
        threading.Thread.__init__(self)
        self.status = False;
        self.statusPressure = False;
        self.pressure = 1;
        self.data = {}
        self.fusionPose = {'x':0,'y':0,'z':0}

        SETTINGS_FILE = "settings/RTIMULib"
        if(code == "Hector"):
            SETTINGS_FILE = SETTINGS_FILE + "_" + code
            print(SETTINGS_FILE);
        self.s = RTIMU.Settings(SETTINGS_FILE)
        self.imu = RTIMU.RTIMU(self.s)
        self.rtpressure = RTIMU.RTPressure(self.s)

        self.imu.IMUInit()
        # if (not self.imu.IMUInit()):
            # print("IMU Init Failed")
            # sys.exit(1)
        # else:
            # print("IMU Init Succeeded");

        self.imu.setSlerpPower(0.02)
        self.imu.setGyroEnable(True)
        self.imu.setAccelEnable(True)
        self.imu.setCompassEnable(True)

        self.rtpressure.pressureInit()
        # if (not self.rtpressure.pressureInit()):
        #     sys.exit(1)
        # # else:
        # #     print("Pressure sensor Init Succeeded")

        self.poll_interval = self.imu.IMUGetPollInterval()
        print("Loaded Imu Sensor");
    def getData(self):
        return self.data
    def getDataFusion(self):
        return self.fusionPose
    def getDataJson(self):
        return json.dumps(self.data)

    def getPressure(self):
        return self.pressure
    def getAltitude(self,P0):
        #P0
        #T0
        #z0 da prendere da getData prima della function
        g=9.81;
        R=287;
        T0=290;
        P=self.pressure;
        if(self.pressure == 0):
            P = 1.
        return (-(R*T0)/g)*math.log(P/P0);
    def uploadData(self):
        flag = True;
        def computeHeight(pressure):
            return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
        while flag:
            if self.imu.IMURead():
                data = self.imu.getIMUData()
                (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = self.rtpressure.pressureRead()

                if data["pressureValid"] != 0 and data["temperatureValid"] != 0:
                    pressure = data['pressure']
                    data["compute_height"] = computeHeight(pressure);
                    flag = False;
                self.data = data;
                # print(math.sqrt(math.pow(self.data['compass'][0],2)+math.pow(self.data['compass'][1],2)+math.pow(self.data['compass'][2],2)));
                self.fusionPose['x'] = self.data['fusionPose'][2]*(180/3.141);
                self.fusionPose['y'] = self.data['fusionPose'][2]*(180/3.141);
                self.fusionPose['z'] = self.data['fusionPose'][2]*(180/3.141);
    def run(self):
        def computeHeight(pressure):
            return 44330.8 * (1 - pow(pressure / 1013.25, 0.190263));
        while True:
            try:
                if self.imu.IMURead():
                    data = self.imu.getIMUData()
                    # print(data['compass'][0])
                    (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = self.rtpressure.pressureRead()
                    if data["pressureValid"] != 0 and data["temperatureValid"] != 0:
                        self.data = data;
                        self.status = True;
                    else:
                        self.status = False;
                    #     self.pressure = data['pressure']
                    #     data["compute_height"] = computeHeight(self.pressure);
                    #     self.fusionPose['x'] = self.data['fusionPose'][2]*(180/3.141);
                    #     self.fusionPose['y'] = self.data['fusionPose'][2]*(180/3.141);
                    #     self.fusionPose['z'] = self.data['fusionPose'][2]*(180/3.141);
                    # print(self.pressure);
                else:
                    self.status = False;
                time.sleep(0.001)
            except KeyboardInterrupt:
                self.status = False;
                time.sleep(3)
