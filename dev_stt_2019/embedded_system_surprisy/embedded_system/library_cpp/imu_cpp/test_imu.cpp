#include "Imu.h"            //Here. Again player.h must be in the current directory. or use relative or absolute path to it.
#include "Imu.cpp"
#include <thread>
#include <memory>
#include <unistd.h>
using namespace std;
int main(){
    Imu imu_sensor;
    // Task * taskPtr = new Task();

	// // Create a thread using member function
	// std::thread th(&Imu::runUpdateData, std::ref(imu_sensor), "Imu Task");
    // th.join();

	// Create a thread using member function
	// std::thread th(&Imu::updateData, std::ref(imu_sensor), "Imu Task");

	// th.join();
    // thread threadObj( (Imu()) );
    // threadObj.join();

    while(1){
        imu_sensor.updateData();
        printf("Pressure:%f\n", imu_sensor.getPressure());
        printf("Temperature:%f\n", imu_sensor.getTemperature());
        printf("FusionPoseZ:%f\n", imu_sensor.getFusionPoseZ());
        // printf("Status:%d\n", imu_sensor.getStatus());
        usleep(100000);
    }
    // delete imu_sensor;
	return 0;
}
