from Imu import Imu
import time


imu_sensor = Imu();
imu_sensor.start();
while True:
    # imu_sensor.uploadData()
    print(imu_sensor.fusionPose['z']);
    time.sleep(0.1)
