'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = this is a python code with raspberry pi 3B to Control ultra sonic sensor HC-SR04 functionality
            = 

'''

from gpiozero import DistanceSensor
from time import sleep

sensor = DistanceSensor(echo=15, trigger=14)
def main():
    sensor = DistanceSensor(echo=15, trigger=14)
    try:
        while True:
            distance = sensor.distance * 100  # convert to cm
            print(f"Distance: {distance:.2f} cm")
            sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by User")

if __name__ == '__main__':
    main()
