#include <Servo.h>

Servo wristServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo thumbServo;
Servo pinkyServo;

void setup() {
  Serial.begin(9600);

  wristServo.attach(2);
  indexServo.attach(10);
  middleServo.attach(11);
  ringServo.attach(12);
  thumbServo.attach(9);
  pinkyServo.attach(6);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command.length() == 6) {
      // Control wrist servo
      wristServo.write(command[0] == '1' ? 180 : 0);

      // Control index finger servo
      indexServo.write(command[1] == '1' ? 180 : 0);

      // Control middle finger servo
      middleServo.write(command[2] == '1' ? 180 : 0);

      // Control ring finger servo
      ringServo.write(command[3] == '1' ? 0 : 180);

      // Control thumb servo
      thumbServo.write(command[4] == '1' ? 0 : 180);

      // Control pinky finger servo
      pinkyServo.write(command[5] == '1' ? 0 : 180);
    }
  }
}
