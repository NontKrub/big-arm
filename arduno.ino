#include <Servo.h>

Servo armServo;      // หยิบโดนัท
Servo baseServo;     // หมุนตามตำแหน่ง
int servoPin1 = 9;
int servoPin2 = 10;

void setup() {
  Serial.begin(9600);
  armServo.attach(servoPin1);
  baseServo.attach(servoPin2);
  armServo.write(90);
  baseServo.write(90);
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 'R') { // วางแดง
      moveTo(30);
    } else if (cmd == 'G') { // วางเขียว
      moveTo(90);
    } else if (cmd == 'B') { // วางน้ำเงิน
      moveTo(150);
    }
  }
}

void moveTo(int angle) {
  baseServo.write(angle);
  delay(500);
  armServo.write(0);   // หยิบ
  delay(800);
  armServo.write(90);  // ปล่อย
  delay(500);
}