from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=15, trigger=14, max_distance = 4, pin_factory = PiGPIOFactory())

def main():
  try:
    while True:
      print('Measured Distance', sensor.distance*100, 'cm')
      sleep(1)
  except KeyboardInterrupt:
    print("Program stopped by User")
  finally:
    quit()

if __name__ == '__main__':
  main()
