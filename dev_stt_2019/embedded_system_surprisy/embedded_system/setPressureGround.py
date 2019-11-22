import time,csv

from library_py.imu_py.Imu import Imu

#Loading Imu Sensor
imu_sensor = Imu();
imu_sensor.daemon = True;
imu_sensor.start();#Update Imu Data

counter = 0;
sum = 0;
while(counter <= 1000):
    if(imu_sensor.status):
        sum = sum + imu_sensor.data["pressure"];
        counter = counter + 1;
    time.sleep(0.001);
pressureGround = sum/counter;
file = "settings/pressure_ground.csv";
with open(file, mode='w') as csv_file:
    fieldnames = ['pressure']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'pressure': pressureGround})
