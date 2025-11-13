'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = this is a python code with raspberry pi 3B to Control SHARP IR sensor GP2Y0A21 through ADC MCP3008 functionality
            = 

'''

from gpiozero import MCP3008
from time import sleep
ir_sensor = MCP3008(0)  # assuming the sensor is connected to channel 0

def main():
#    ir_sensor = MCP3008(channel=0)
    try:
        while True:
            voltage = ir_sensor.value * 3.3  # convert to voltage (assuming 3.3V reference)
            #distance_cm = 27.86 / (voltage - 0.42)  # example conversion formula
            print(f"IR Sensor Voltage: 0.2f",ir_sensor.value)
#, Distance: {distance_cm:.2f} cm")
            sleep(1)
    except KeyboardInterrupt:
        print("Program stopped by User")

if __name__ == '__main__':
	main()
