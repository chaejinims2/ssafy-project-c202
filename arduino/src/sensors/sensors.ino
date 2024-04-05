#include<Wire.h>
#include "DHT.h"

// Constants
#define MPU6050_ADDR 0x68   
#define MPU6050_PWR_MGMT 0x6B
#define MPU6050_GYRO_REG 0x1b
#define MPU6050_ACCL_REG 0x1c
#define DHTPIN 1     // what digital pin we're connected to
#define DHTTYPE DHT11   // DHT 11

// Variables
int16_t aX, aY, aZ, Tmp, gX, gY, gZ;
float aX_g, aY_g, aZ_g, ttt, gX_dps, gY_dps, gZ_dps;
float h, t;
DHT dht(DHTPIN, DHTTYPE);
unsigned long lastDHTCheck = 0;

void setup() {
    // Setup for MPU-6050
    Wire.begin();
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(MPU6050_PWR_MGMT);  // PWR_MGMT_1 register
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

    // Setup for DHT sensor
    dht.begin();

    // Setup for Serial communication
    Serial.begin(115200);
}

void loop() {
    // Read from DHT sensor every 2 seconds
    if (millis() - lastDHTCheck >= 2000) {
        h = dht.readHumidity();
        t = dht.readTemperature();

        // Check if readings are valid
        if (isnan(h) || isnan(t)) {
            Serial.println("Failed to read from DHT sensor!");
        } else {
            // Print DHT readings
            // Serial.print("T/H = "); Serial.print(t); Serial.print(" *C, "); Serial.print(h); Serial.print(" %, ");
        }

        lastDHTCheck = millis();
    }

    // Read from MPU-6050
    Wire.beginTransmission(MPU6050_ADDR);
    Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
    Wire.endTransmission(false);
    Wire.requestFrom(MPU6050_ADDR,14,true);  // request a total of 14 registers
    aX = Wire.read()<<8 | Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
    aY = Wire.read()<<8 | Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
    aZ = Wire.read()<<8 | Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
    Tmp = Wire.read()<<8 | Wire.read();  // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)
    gX = Wire.read()<<8 | Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
    gY = Wire.read()<<8 | Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
    gZ = Wire.read()<<8 | Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)

    // Convert raw values to g's and degrees per second
    
    
    aX_g = aX / 32768.0 * 16;
    aY_g = aY / 32768.0 * 16;
    aZ_g = aZ / 32768.0 * 16;
    gX_dps = gX / 32768.0 * 1000;
    gY_dps = gY / 32768.0 * 1000;
    gZ_dps = gZ / 32768.0 * 1000;
    ttt = Tmp/340.00+36.53;

    
    Serial.print(aX); Serial.print(",");
    Serial.print(aY); Serial.print(",");
    Serial.print(aZ); Serial.print(",");
    Serial.print(gX); Serial.print(",");
    Serial.print(gY); Serial.print(",");
    Serial.print(gZ); Serial.print(",");
    Serial.print(Tmp); Serial.print(",");
    Serial.print(t); Serial.print(",");
    Serial.println(h);
    // Print MPU-6050 readings
    // Serial.print("aX = "); Serial.print(aX); Serial.print(", ");
    // Serial.print("aY = "); Serial.print(aY); Serial.print(", ");
    // Serial.print("aZ = "); Serial.print(aZ); Serial.print(", ");

    // Serial.print("Tmp = "); Serial.print(Tmp); Serial.print(", ");  //equation for temperature in degrees C from datasheet
    // Serial.print("gX = "); Serial.print(gX); Serial.print(", ");
    // Serial.print("gY = "); Serial.print(gY); Serial.print(", ");
    // Serial.print("gZ = "); Serial.println(gZ);

    // // Print MPU-6050 readings
    // Serial.print("aX = "); Serial.print(aX_g); Serial.print(" g, ");
    // Serial.print("aY = "); Serial.print(aY_g); Serial.print(" g, ");
    // Serial.print("aZ = "); Serial.print(aZ_g); Serial.print(" g, ");
    // Serial.print("tp = "); Serial.print(ttt); Serial.print(" °C, ");  //equation for temperature in degrees C from datasheet
    // Serial.print("gX = "); Serial.print(gX_dps); Serial.print(" °/s, ");
    // Serial.print("gY = "); Serial.print(gY_dps); Serial.print(" °/s, ");
    // Serial.print("gZ = "); Serial.println(gZ_dps); Serial.print(" °/s");

}