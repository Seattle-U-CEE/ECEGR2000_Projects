# Ultrasonic 
The HC-SR04 sensor measures the round-trip travel time for a pulse of sound emitted by an ultrasonic speaker to return to the device. The travel time divided by the speed of sound gives the round-trip distance. It can be used to estimate proximity and/or movement.  Note that anything that reflects sound can, in principle, be detected by the sensor. This includes liquid/air interfaces (e.g., a fluid surface) as well as solid objects.

The [GPIOZero Library Distance Sensor Class](https://gpiozero.readthedocs.io/en/stable/api_input.html#distancesensor-hc-sr04) provides methods that simplify the use of the sensor.

## Wiring diagram

Using the following parts:

- RaspberryPi
- 1kOhms Resistor
- 2kOmhs Resistor
- wires
- prototype board

![diagram](./hc-sr04-tut-2_1024x1024.png "diagram" )

## Run the Program

```
python distance.py
``` 
