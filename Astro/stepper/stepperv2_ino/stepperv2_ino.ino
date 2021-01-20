#include <MultiStepper.h>
#include <AccelStepper.h>
// DRV8825

//#define MOTOR_137 // 1:3.7 reducer on NEMA 17
#define MOTOR_1139 // 1:139 reducer on NEMA 17
//#define MOTOR_11 // small NEMA 17 without reducer

#define disablepin 6
#define dirPin 5
#define stepPin 3
#define microPin 4
#define motorInterfaceType 1

#define stepsperruns 1


#ifdef MOTOR_137
const long stepsPerRevolution = 200*3.7;
#endif
#ifdef MOTOR_1139
const long stepsPerRevolution = 200*139;
#endif
#ifdef MOTOR_11
const long stepsPerRevolution = 200;
#endif

long steps = stepsperruns;

size_t state = 0;
AccelStepper stepper = AccelStepper(motorInterfaceType, stepPin, dirPin);

volatile bool buttonInterrupt = false;
void buttonPushed() {
    stepper.stop();
    buttonInterrupt = true;
}

void reset() {
  Serial.println("Reset");
  digitalWrite(disablepin, HIGH);
  state=0;
  stepper.setCurrentPosition(0);
  digitalWrite(microPin, LOW); // set x32 micro stepping
  steps = stepsperruns;
}

void setup() {
  pinMode(disablepin, OUTPUT);
  pinMode(microPin, OUTPUT);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(INT0, buttonPushed, FALLING);
  digitalWrite(microPin, LOW);
  digitalWrite(disablepin, HIGH);
  Serial.begin(9600);
  
  #ifdef MOTOR_137
  stepper.setMaxSpeed(50*16); // full stepping max: 50*16
  stepper.setAcceleration(15*8); // full stepping max: 15*8
  #endif
  #ifdef MOTOR_1139
  stepper.setMaxSpeed(50*32); // full stepping max: 50*32
  stepper.setAcceleration(15*16); // full stepping max: 15*16
  #endif
  #ifdef MOTOR_11
  stepper.setMaxSpeed(30); // full stepping max: 30
  stepper.setAcceleration(10); // full stepping max: 10
  #endif
  reset();
}
void loop() {
  if (buttonInterrupt) {
    delay(500); // debounce
    if(!digitalRead(2)) // button still push, loop and wait again
      return;
    buttonInterrupt = false;
    Serial.println("RESET");
    // change state
    state = 0;
    reset();
  }
  
  if (state == 0) {
    if (Serial.available() > 0) {
      int incomingByte = Serial.read();
      Serial.println((char)incomingByte);
      if(incomingByte >= '0' && incomingByte <= '9') {
        state = incomingByte - '0';
        Serial.print("Going to state ");
        Serial.println(state);
      }
    }
  }
  else if (state == 1) {
    digitalWrite(microPin, LOW); // set full steps
    digitalWrite(disablepin, LOW);
    Serial.println("-");
    Serial.print("current position ");
    Serial.println(stepper.currentPosition());
    
    long todo = steps*stepsPerRevolution;
    Serial.print("going to ");
    Serial.println(todo);
    
    stepper.moveTo(todo);
    stepper.runToPosition();
    delay(500);
    Serial.print("Turn #");
    Serial.print(steps);
    Serial.println("done");
    steps += stepsperruns;
    delay(500);
    
  } else if (state == 2) {
    digitalWrite(microPin, HIGH); // set x32 micro stepping
    digitalWrite(disablepin, LOW);
    float targetspeed = (200.0*139*32.0)/(10.0*60.0); // steps per seconds = 1 turn per 10 min
    stepper.setSpeed(targetspeed);
    Serial.println("Run speed looping");
    stepper.runSpeed();
    state = 20;
  } else if (state == 20) {
    stepper.runSpeed();
  } else if (state == 3) {
    
    #ifdef MOTOR_11
    stepper.setMaxSpeed(30*32); // micro stepping max: 30*32
    stepper.setAcceleration(10*32); // micro stepping max: max: 10*32
    #endif
    #ifdef MOTOR_137
    stepper.setMaxSpeed(50*16*32); // micro stepping max: max: 50*16*32
    stepper.setAcceleration(15*8*32); // micro stepping max: max: 15*8*32
    #endif
    #ifdef MOTOR_1139
    stepper.setMaxSpeed(50*32*16); // micro stepping max: 50*32*32
    stepper.setAcceleration(15*16); // micro stepping max: 15*16*32
    #endif
    
    digitalWrite(microPin, HIGH); // set x32 micro stepping
    digitalWrite(disablepin, LOW);
    Serial.println("-");
    Serial.print("current position ");
    Serial.println(stepper.currentPosition());
    
    long todo = 32*steps*stepsPerRevolution;
    Serial.print("going to ");
    Serial.println(todo);
    
    stepper.moveTo(todo);
    stepper.runToPosition();
    delay(500);
    Serial.print("Turn #");
    Serial.print(steps);
    Serial.println("done");
    steps += stepsperruns;
    delay(500);
  }
}
