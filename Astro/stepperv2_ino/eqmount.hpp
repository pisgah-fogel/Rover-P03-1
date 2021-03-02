#include "Arduino.hpp"

#define stepper_pin_step 3
#define stepper_pin_dir 5
#define stepper_pin_disable 6 // LOW = power motor
#define stepper_pin_micro 4 // LOW = x32 microstepping
#define stepper_minpulsewidth 1 // minimum pulse width in micro second
#define stepper_dir_clockwise HIGH
#define stepper_dir_reverse LOW
#define stepper_micro_off HIGH // Do not use microstepping
#define stepper_micro_x32 LOW // Use microstepping

long position; // steps (positive is clockwise)
char direction; // HIGH = clockwise
unsigned long lasttimestep; // last time we did a step, in microsecond
float speed; // steps per second
float acceleration; // steps per second per second
float targetspeed; // steps per seconds
unsigned long stepDelay; // required delay between to steps, in microsecond
float maxAcceleration = 15*16*1000;
float speedok_threshold = 1.0;

void onestep() {
    digitalWrite(stepper_pin_dir, direction);
    digitalWrite(stepper_pin_step, HIGH);
    delayMicroseconds(stepper_minpulsewidth);
    if(direction == stepper_dir_clockwise)
        position++;
    else
        position--;
    digitalWrite(stepper_pin_step, LOW);
    lasttimestep = micros();
}

inline void eq_maintain_speed()
{
    motorManagerLoop();
}

// You should set targetspeed before calling this function
// And call enableMotor() / disableMotor()
// digitalWrite(stepper_pin_step, direction);
// stepDelay = 100000;
// lasttimestep = micros();
bool motorManagerLoop() {
    unsigned long interval = micros() - lasttimestep;
    bool ret = false;
    if (interval >= stepDelay) {
        onestep();

        // calcul actual speed
        speed = 1000000 / interval;

        float error = targetspeed - speed;

        //Serial.print("Error ");
        //Serial.println(error);

        acceleration = 100.0*error;

        if (acceleration > maxAcceleration)
            acceleration = maxAcceleration;
        if (acceleration < -maxAcceleration)
            acceleration = -maxAcceleration;

        if ((micros() >> 1) << 1 % 2000000 == 0) {
            Serial.print("speed ");
            Serial.println(speed);
            Serial.print("error ");
            Serial.println(error);
            Serial.print("acceleration ");
            Serial.println(acceleration);
        }

        if (error < speedok_threshold)
            ret = true;
        
        //Serial.print("acceleration ");
        //Serial.println(acceleration);

        // wait accordinly
        stepDelay = (float)((float)interval - (float)interval*acceleration/1000000.0);
        //delayMicroseconds(stepDelay-8); // TODO: remove this and do something usefull instead
    }
    return ret;
}

// blocking
void reachTargetSpeed(float target, float thrs) {
    speedok_threshold = thrs;
    targetspeed = target;
    enableMotor();
    Serial.println("Motor enabled");
    stepDelay = 100000; // will be overwritten anyway, should not be too big
    lasttimestep = micros();
    while (!motorManagerLoop());
}

// blocking
void stopMotor() {
    Serial.println("Slowing down");
    targetspeed = 0;
    while (!motorManagerLoop());
    Serial.println("Motor stopped");
    disableMotor();
}

inline void disableMotor() {
    digitalWrite(stepper_pin_disable, HIGH);
}

inline void enableMotor() {
    digitalWrite(stepper_pin_disable, LOW);
}

inline void setMotorFullStep() {
    digitalWrite(stepper_pin_micro, stepper_micro_off);
}

inline void setMotorMicroStep() {
    digitalWrite(stepper_pin_micro, stepper_micro_x32);
}

void eq_setup()
{
    // Initialize
    position = 0;
    direction = stepper_dir_clockwise;
    speed = 0;
    acceleration = 0;
    lasttimestep = 0;
    targetspeed = 0;

    // Init motor
    pinMode(stepper_pin_step, OUTPUT); digitalWrite(stepper_pin_step, LOW);
    pinMode(stepper_pin_dir, OUTPUT); digitalWrite(stepper_pin_step, direction);
    pinMode(stepper_pin_disable, OUTPUT); disableMotor();
    pinMode(stepper_pin_micro, OUTPUT); setMotorFullStep();
    // max speed full steps: 50*32
    // max speed micro steps: 50*32*16
    // max acceleration full steps: 15*16
    // max acceleration micro steps: 15*16
}