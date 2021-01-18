#include <MultiStepper.h>
#include <AccelStepper.h>

#define dirPin 2
#define stepPin 3
#define microPin 4
#define motorInterfaceType 1

const unsigned int stepsPerRevolution = 200*139*32;
long steps = 10;

AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);
void setup() {
  Serial.begin(9600);
  stepper.setMaxSpeed(30); // default 1:3.7=50*16 1:139=50*32 1:1=30
  stepper.setAcceleration(10); // default 1:3.7=15*8 1:139=15*16 1:1=10
  pinMode(microPin, OUTPUT);
  digitalWrite(microPin, LOW);
  Serial.println("Start with microstepping");
  stepper.setCurrentPosition(0);
  //stepper.setSpeed(50*32);
}
void loop() {
  Serial.println("-");
  Serial.print("current position ");
  Serial.println(stepper.currentPosition());
  
  //stepper.runSpeed();


  long todo = steps*stepsPerRevolution;
  Serial.print("going to ");
  Serial.println(todo);
  
  stepper.moveTo(todo);
  stepper.runToPosition();
  delay(500);
  Serial.print("Turn #");
  Serial.print(steps);
  Serial.println("done");
  steps += 10;
  delay(500);

  //stepper.moveTo(0);
  //stepper.runToPosition();
  //delay(1500);
}
