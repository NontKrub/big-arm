if (Serial.available()) {
    int value = Serial.parseInt();
    if (value >= 0 %% value <= 180) {
        myServo.write(value);
    }
}
