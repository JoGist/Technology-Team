#include "Imu.h"


Imu::Imu() {
    RTIMUSettings *settings = new RTIMUSettings("RTIMULib");

    RTimu = RTIMU::createIMU(settings);
    RTpressure = RTPressure::createPressure(settings);
    if ((RTimu == NULL) || (RTimu->IMUType() == RTIMU_TYPE_NULL)) {
        printf("No IMU found\n");
        exit(1);
    }
    RTimu->IMUInit();

    //  this is a convenient place to change fusion parameters

    RTimu->setSlerpPower(0.02);
    RTimu->setGyroEnable(true);
    RTimu->setAccelEnable(true);
    RTimu->setCompassEnable(true);

    //  set up pressure sensor

    if (RTpressure != NULL)
        RTpressure->pressureInit();
}
void Imu::updateData() {
    // usleep(RTimu->IMUGetPollInterval() * 1000);
    if (RTimu->IMURead()) {
        RTIMU_DATA RTimuData = RTimu->getIMUData();
        if (RTpressure != NULL)
            RTpressure->pressureRead(RTimuData);

        printf("Sample rate : %f\n", RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE);
        fusionPoseZ = RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE;
        if (RTpressure != NULL) {
            pressure = RTimuData.pressure;
            temperature = RTimuData.temperature;
            // printf("Pressure: %4.1f, height above sea level: %4.1f, temperature: %4.1f\n",
                   // RTimuData.pressure, RTMath::convertPressureToHeight(RTimuData.pressure), RTimuData.temperature);
        }

    }
}

void Imu::operator()() {
    while(1){
        if (RTimu->IMURead()) {
            RTIMU_DATA RTimuData = RTimu->getIMUData();
            if (RTpressure != NULL)
                RTpressure->pressureRead(RTimuData);

            // printf("Sample rate : %f\n", RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE);
            fusionPoseZ = RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE;
            if (RTpressure != NULL) {
                pressure = RTimuData.pressure;
                temperature = RTimuData.temperature;
                // printf("Pressure: %4.1f, height above sea level: %4.1f, temperature: %4.1f\n",
                       // RTimuData.pressure, RTMath::convertPressureToHeight(RTimuData.pressure), RTimuData.temperature);
            }
        }
        usleep(100000);

    }
};
double Imu::getPressure() {
    return pressure;
}
double Imu::getTemperature() {
    return temperature;
}
double Imu::getFusionPoseZ() {
    return fusionPoseZ;
}

void Imu::greeting(){
    int k = 0;
    while(true){
        if (RTimu->IMURead()) {
            RTIMU_DATA RTimuData = RTimu->getIMUData();
            if (RTpressure != NULL)
                RTpressure->pressureRead(RTimuData);

            printf("Sample rate : %f\n", RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE);
            fusionPoseZ = RTimuData.fusionPose.z()*RTMATH_RAD_TO_DEGREE;
            if (RTpressure != NULL) {
                pressure = RTimuData.pressure;
                temperature = RTimuData.temperature;
                // printf("Pressure: %4.1f, height above sea level: %4.1f, temperature: %4.1f\n",
                       // RTimuData.pressure, RTMath::convertPressureToHeight(RTimuData.pressure), RTimuData.temperature);
            }
            printf("_%d",k);
            k++;
        }
        usleep(10000);

    }
}
