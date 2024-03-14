#include "Wire.h"
 #include <MPU6050_light.h>
 
 MPU6050 mpu(Wire);
 
 void setup() {
   Serial.begin(9600);
   Wire.begin();
   byte status = mpu.begin();
   Serial.print(F("MPU6050 durumu: "));
   Serial.println(status);
   while (status != 0) { } // stop everything if could not connect to MPU6050
   Serial.println(F("Kalibrasyon yapılıyor. Lütfen cihazı hareket ettirmeyiniz!"));
   delay(1000);
   mpu.calcOffsets(); // gyro ve açı sensörünün offsetlerini tanımlayalım.
   Serial.println("Kalibrasyon tamamlandı!\n");
 }
 void loop() {
   mpu.update();
   Serial.print("");
   Serial.print(mpu.getAngleX());
   Serial.print(" ");
   Serial.print(mpu.getAngleY());
   Serial.print(" ");
   Serial.println(mpu.getAngleZ());
 }