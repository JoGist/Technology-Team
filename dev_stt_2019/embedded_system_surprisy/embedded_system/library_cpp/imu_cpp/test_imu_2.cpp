#include "Imu.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "Imu.cpp"
#include <thread>
// #include <memory>
// #include <unistd.h>
using namespace std;

int main(){
    Imu imu_sensor;
    std::thread t(&Imu::greeting,&imu_sensor);
    t.join();

    Imu imu_sensor2;
    std::thread t2(&Imu::greeting,&imu_sensor2);
    t2.join();
    // while(1){
    //     // imu_sensor->updateData();
    //     printf("Pressure:%f\n", imu_sensor.getPressure());
    //     printf("Temperature:%f\n", imu_sensor.getTemperature());
    //     printf("FusionPoseZ:%f\n", imu_sensor.getFusionPoseZ());
    //     // printf("Status:%d\n", imu_sensor.getStatus());
    //     // usleep(100000);
    // }
    // delete imu_sensor;
	return 0;
}
