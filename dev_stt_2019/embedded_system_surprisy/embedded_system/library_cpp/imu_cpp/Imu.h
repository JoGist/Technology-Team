#ifndef IMU_H    // To make sure you don't declare the function more than once by including the header multiple times.
#define IMU_H

#include "RTIMULib/RTIMULib.h"
#include "RTIMULib/RTIMUSettings.h"
#include "RTIMULib/RTIMUSettings.cpp"
#include "RTIMULib/RTIMUHal.h"
#include "RTIMULib/RTIMUHal.cpp"
#include "RTIMULib/RTMath.h"
#include "RTIMULib/RTMath.cpp"
#include "RTIMULib/IMUDrivers/RTIMU.h"
#include "RTIMULib/IMUDrivers/RTIMU.cpp"
#include "RTIMULib/IMUDrivers/RTIMUNull.h"
#include "RTIMULib/IMUDrivers/RTIMUNull.cpp"
#include "RTIMULib/IMUDrivers/RTIMUMPU9150.h"
#include "RTIMULib/IMUDrivers/RTIMUMPU9150.cpp"
#include "RTIMULib/IMUDrivers/RTIMUMPU9250.h"
#include "RTIMULib/IMUDrivers/RTIMUMPU9250.cpp"
#include "RTIMULib/IMUDrivers/RTIMUGD20HM303D.h"
#include "RTIMULib/IMUDrivers/RTIMUGD20HM303D.cpp"
#include "RTIMULib/IMUDrivers/RTIMUGD20M303DLHC.h"
#include "RTIMULib/IMUDrivers/RTIMUGD20M303DLHC.cpp"
#include "RTIMULib/IMUDrivers/RTIMUGD20HM303DLHC.h"
#include "RTIMULib/IMUDrivers/RTIMUGD20HM303DLHC.cpp"
#include "RTIMULib/IMUDrivers/RTIMULSM9DS0.h"
#include "RTIMULib/IMUDrivers/RTIMULSM9DS0.cpp"
#include "RTIMULib/IMUDrivers/RTIMULSM9DS1.h"
#include "RTIMULib/IMUDrivers/RTIMULSM9DS1.cpp"
#include "RTIMULib/IMUDrivers/RTIMUBMX055.h"
#include "RTIMULib/IMUDrivers/RTIMUBMX055.cpp"
#include "RTIMULib/IMUDrivers/RTIMUBNO055.h"
#include "RTIMULib/IMUDrivers/RTIMUBNO055.cpp"
#include "RTIMULib/IMUDrivers/RTPressure.h"
#include "RTIMULib/IMUDrivers/RTPressure.cpp"
#include "RTIMULib/IMUDrivers/RTPressureBMP180.h"
#include "RTIMULib/IMUDrivers/RTPressureBMP180.cpp"
#include "RTIMULib/IMUDrivers/RTPressureLPS25H.h"
#include "RTIMULib/IMUDrivers/RTPressureLPS25H.cpp"
#include "RTIMULib/IMUDrivers/RTPressureMS5611.h"
#include "RTIMULib/IMUDrivers/RTPressureMS5611.cpp"
#include "RTIMULib/IMUDrivers/RTPressureMS5637.h"
#include "RTIMULib/IMUDrivers/RTPressureMS5637.cpp"

#include "RTIMULib/RTIMULibDefs.h"
#include "RTIMULib/RTIMUCalDefs.h"
#include "RTIMULib/RTIMUAccelCal.h"
#include "RTIMULib/RTFusion.h"
#include "RTIMULib/RTFusion.cpp"
#include "RTIMULib/RTFusionKalman4.h"
#include "RTIMULib/RTFusionKalman4.cpp"
#include "RTIMULib/RTFusionRTQF.h"
#include "RTIMULib/RTFusionRTQF.cpp"
#include "RTIMULib/RTIMUMagCal.h"
#include "RTIMULib/RTIMUMagCal.cpp"

#define	RTMATH_PI					3.1415926535
#define	RTMATH_DEGREE_TO_RAD		(RTMATH_PI / 180.0)
#define	RTMATH_RAD_TO_DEGREE		(180.0 / RTMATH_PI)

class Imu {
 private:
     RTIMU *RTimu;
     RTPressure *RTpressure;
     double pressure;
     double temperature;
     double fusionPoseZ;

 public:
     Imu();
     void operator()() ;
     void updateData();
     double getPressure();
     double getTemperature();
     double getFusionPoseZ();
     void greeting();

};

#endif
