#include "Gps.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "Gps.cpp"

#include <stdio.h>

int main(){
    Gps gps_sensor;
    int k = 0;
    while(1){
        gps_sensor.updateData();
        printf("Latitude:%f\n", gps_sensor.getLatitude());
        printf("Longitude:%f\n", gps_sensor.getLongitude());
        printf("Status:%d\n", gps_sensor.getStatus());
    }

    return 0;
}
