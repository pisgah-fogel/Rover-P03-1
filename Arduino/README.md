# Arduino directory

## Servo Test

### Result

The Servo Arduino library use:

- 0 degres: T=20ms, Th=0.6ms
- 45 degres: T=20ms, Th=1.0ms
- 90 degres: T=20ms, Th=1.6ms
- 180 degres: T=20ms, Th=2.5ms

Therefore to mimic this behavior you can use:
```python
def angles_to_pwm(a):
	return a*1.9/180+0.6
```

## DC motor Test

### Wiring
- Wire 1 (Black and Red): Power Alim + (+5 to +12V)
- Wire 2: +5V for sensor
- Wire 3: Square signal representing the motor speed
- Wire 4: Square signal representing the motor speed
- Wire 5: Ground for sensor
- Wire 6: Power Ground
