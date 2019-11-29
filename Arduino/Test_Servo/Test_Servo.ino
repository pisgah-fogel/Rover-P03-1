#include <Servo.h>

Servo dut; // Device under test

void setup() {
  dut.attach(6);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  dut.write(0);
  delay(5000);

  dut.write(45);
  digitalWrite(LED_BUILTIN, LOW);
  delay(5000);
}
