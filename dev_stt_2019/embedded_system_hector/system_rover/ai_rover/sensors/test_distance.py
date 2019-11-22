
from DistanceSensor import DistanceSensor

print ("Test Distance")
distance_sensor = DistanceSensor();
while(True):
    distance_sensor.uploadData();
    print(distance_sensor.getData())
