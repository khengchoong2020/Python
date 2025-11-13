'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = This is a python code with raspberry pi 3B to Control PIR sensor functionality
            = 

'''

from gpiozero import MotionSensor       
from time import sleep
pir = MotionSensor(4)    # GPIO4
def main():
#    pir = MotionSensor(4)
    try:
        while True:
            pir.wait_for_motion()
            print("Motion detected!")
            pir.wait_for_no_motion()
            print("No motion")
    except KeyboardInterrupt:
        print("Program stopped by User")    

if __name__ == '__main__':
	main()
