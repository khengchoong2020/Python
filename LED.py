'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = this is a python code with raspberry pi 3B to Control LED functionality


'''

from gpiozero import LED
from time import sleep

led = LED(17)
def main():
    led = LED(17)
    try:
        while True:
            led.on()
            sleep(1)
            led.off()
            sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        led.off()
        print("LED turned off")


if __name__ == '__main__':
    main()