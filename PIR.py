'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = This is a python code with raspberry pi 3B to Control PIR sensor functionality
            = PIR (Passive Infrared) sensor detects motion using infrared radiation
            = GPIO 4 on Raspberry Pi 3B
'''

from gpiozero import MotionSensor
from time import sleep

# Initialize PIR sensor on GPIO 4 with debounce time to avoid false triggers
pir = MotionSensor(4, queue_len=1, sample_rate=10, threshold=0.5)

def main():
    """
    Main loop to monitor PIR sensor for motion detection.
    Blocks until motion is detected, then waits for no motion.
    """
    try:
        print("PIR Sensor initialized on GPIO 4")
        print("Waiting for motion detection...")
        
        while True:
            pir.wait_for_motion()
            print("Motion detected!")
            
            pir.wait_for_no_motion()
            print("No motion detected")
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup GPIO resources
        pir.close()
        print("PIR sensor cleanup completed")

if __name__ == '__main__':
    main()
