from Gps import Gps
import time

gps_sensor = Gps();
gps_sensor.daemon = True;
gps_sensor.start();
targetData = gps_sensor.getTargetData("data_gps_target.csv",0);
print(targetData);
while(True):
    print(gps_sensor.status);
    time.sleep(1);
