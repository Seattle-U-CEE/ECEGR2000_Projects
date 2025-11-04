from gpiozero import DistanceSensor
from time import sleep

# Set up the sensor (echo and trigger pin, here GPIO pin 24 for ECHO, pin 23 for TRIG)
sensor = DistanceSensor(echo=24, trigger=23)

print("Distance Measurement In Progress")
sleep(2)  # Wait for the sensor to settle

while True:
    # Read distance
    distance_cm = sensor.distance * 100  # sensor.distance gives meters
    print(f"Distance: {distance_cm:.2f} cm")
