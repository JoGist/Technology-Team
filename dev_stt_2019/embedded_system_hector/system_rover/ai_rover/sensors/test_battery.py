from Battery import Battery

print ("Test Encoder")
battery = Battery();
while(True):
    battery.updateMeasurement();
    print(battery.getVoltage())
