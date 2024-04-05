#include <mpu9250.h>


#include<Wire.h>

#define MPU6050_ADDR 0x69   
// #define MPU6050_PWR_MGMT 0x6B
#define MPU6050_GYRO_REG 0x44
#define MPU6050_ACCL_REG 0x3c
#define MPU6050_MAGN_REG 0x04
MPU9250 mpu;

void setup() {
    Serial.begin(115200);
    Wire.begin();
    delay(2000);
    // Setup for MPU-6050
    Wire.begin();
    Wire.beginTransmission(MPU6050_ADDR);
    // Wire.write(MPU6050_PWR_MGMT);  // PWR_MGMT_1 register
    Wire.write(0);     // set to zero (wakes up the MPU-6050)
    Wire.endTransmission(true);

    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(MPU6050_GYRO_REG);  // GYRO_CONFIG register
    Wire.write(2);     // set to 2 (±1000 °/s)
    Wire.endTransmission(true);

    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(MPU6050_ACCL_REG);  // ACCEL_CONFIG register
    Wire.write(3);     // set to 3 (±16 g)
    Wire.endTransmission(true);


    //print_calibration();
    mpu.verbose(false);
}





void loop() {
    if (mpu.update()) {
        static uint32_t prev_ms = millis();
        if (millis() > prev_ms + 25) {
            
            print_rawdata();
            
            //print_roll_pitch_yaw();
            prev_ms = millis();
        }
    }
}

void print_rawdata(void)
{  
  float aX = mpu.getAccX();
  float aY = mpu.getAccY();
  float aZ = mpu.getAccZ();
  float gX = mpu.getGyroX();
  float gY = mpu.getGyroY();
  float gZ = mpu.getGyroZ();
  
    
  Serial.print(aX); Serial.print(",");
  Serial.print(aY); Serial.print(",");
  Serial.print(aZ); Serial.print(",");
  Serial.print(gX); Serial.print(",");
  Serial.print(gY); Serial.print(",");
  Serial.print(gZ); Serial.println(",");
  
}


