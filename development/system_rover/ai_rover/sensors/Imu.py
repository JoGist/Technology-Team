# import sys
# sys.path.append('.')
import RTIMU, json, time
import multiprocessing

class Imu():
    def __init__(self, timestamp=0, accel=[], gyro=[], compass=[]):
        self.timestamp = timestamp
        self.accel = accel
        self.gyro = gyro
        self.compass = compass
        self.data = {}
        SETTINGS_FILE = "RTIMULib"

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
                    self.data = data;
                    flag = False;
                # print(data)
    def getData(self):
        flag = True;
        while flag:
            if self.imu.IMURead():
                data = self.imu.getIMUData()
                (data["pressureValid"], data["pressure"], data["temperatureValid"], data["temperature"]) = self.rtpressure.pressureRead()

                if data["pressureValid"] != 0 and data["temperatureValid"] != 0:
                    print(data)
                    return data;
                    flag = False;
    def getData(self):
        return self.data
    def getDataJson(self):
        return json.dumps(self.data)
    def updateData(self):
        while True:
            self.uploadData()
            print(self.getData()['gyro'])
            time.sleep(0.001)
            pass
    def auto_update(self):
        process = multiprocessing.Process(target=self.updateData, args=())
        process.daemon = True
        process.start()
