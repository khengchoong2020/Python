'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = this is a python code with raspberry pi 3B to Control SG90 microservo functionality
            = by turning angle from 0 to 180 degrees using pigpio library
            = SG90 specs: min = 0.6ms (500µs), max = 2.4ms (2500µs) pulse width, mid = 1.5ms

'''

import pigpio
import time

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")

# GPIO pin for servo
SERVO_PIN = 18

def set_angle(angle):
    """
    Convert angle to pulse width and set servo position
    angle: 0-180 degrees
    pulse width: 500-2500 microseconds
    """
    if not 0 <= angle <= 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    
    # Convert angle to pulse width (microseconds)
    # 500µs (0°) to 2500µs (180°)
    pulse_width = int(500 + (angle * 2000 / 180))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

# Test the servo movement
def test_servo():
    print("Moving to 0 degrees")
    set_angle(0)
    time.sleep(1)
    
    print("Moving to 90 degrees")
    set_angle(90)
    time.sleep(1)
    
    print("Moving to 180 degrees")
    set_angle(180)
    time.sleep(1)

def main():
    try:
        while True:
            print("Moving to minimum position (0°)")
            set_angle(0)
            time.sleep(1)
            
            print("Moving to middle position (90°)")
            set_angle(90)
            time.sleep(1)
            
            print("Moving to maximum position (180°)")
            set_angle(180)
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by User")
    finally:
        # Move to neutral position and cleanup
        print("Moving to neutral position")
        set_angle(90)
        time.sleep(0.5)
        # Stop sending pulses
        pi.set_servo_pulsewidth(SERVO_PIN, 0)
        # Cleanup
        pi.stop()
        print("Cleanup completed")

if __name__ == '__main__':
    main()