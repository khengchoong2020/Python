from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=15, trigger=14, max_distance = 4, pin_factory = PiGPIOFactory())

while True:
  try:
    print('Measured Distance', sensor.distance, 'm')
    sleep(1)
  except KeyboardInterrupt:
    quit()
