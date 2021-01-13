const int dirPin = 2;
const int stepPin = 3;
const int stepsPerRevolution = 200*3.7;

void setup()
{
	// Declare pins as Outputs
	pinMode(stepPin, OUTPUT);
	pinMode(dirPin, OUTPUT);
        pinMode(13, OUTPUT);
        digitalWrite(13, HIGH);
}
void loop()
{
	// Set motor direction clockwise
	digitalWrite(dirPin, HIGH);
        digitalWrite(13, LOW);

	// Spin motor slowly
	for(int x = 0; x < stepsPerRevolution; x++)
	{
		digitalWrite(stepPin, HIGH);
		//delayMicroseconds(2000);
                delay(10);
		digitalWrite(stepPin, LOW);
                delay(10);
	}
	delay(1000); // Wait a second
        digitalWrite(13, HIGH);
        delay(1000); // Wait a second
}
