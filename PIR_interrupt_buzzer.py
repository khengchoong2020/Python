'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-15
Description = Event-based interrupt handling for PIR sensor using gpiozero library
            = Uses callback functions (when_motion and when_no_motion) for non-blocking motion detection
            = GPIO 4 on Raspberry Pi 3B
            = Allows the main program to continue running while monitoring PIR sensor
'''

from gpiozero import MotionSensor, PWMOutputDevice
from time import sleep
import time

# Initialize PIR sensor on GPIO 4 with debounce to avoid false triggers
pir = MotionSensor(4, queue_len=1, sample_rate=10, threshold=0.5)
buzzer = PWMOutputDevice(22, frequency=440, initial_value=0)

# Global state tracking
motion_detected_time = 0
motion_count = 0
last_motion_event = None


def on_motion():
    """
    Callback function triggered when motion is detected.
    This runs asynchronously without blocking the main loop.
    """
    global motion_detected_time, motion_count, last_motion_event
    motion_detected_time = time.time()
    motion_count += 1
    last_motion_event = "Motion"
    print(f"[INTERRUPT] Motion detected! (Event #{motion_count})")
    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime(motion_detected_time))}")
    for _ in range(10):
        buzzer.value = 1.0  # Turn on buzzer
        sleep(0.1)
        buzzer.value = 0    # Turn off buzzer
        sleep(0.1)



def on_no_motion():
    """
    Callback function triggered when motion stops.
    This runs asynchronously without blocking the main loop.
    """
    global last_motion_event
    last_motion_event = "No Motion"
    print(f"[INTERRUPT] No motion detected")
    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime())}")



def get_motion_status():
    """
    Non-blocking function to get current motion status.
    Returns: True if motion detected, False otherwise
    """
    return pir.motion_detected


def main():
    """
    Main loop demonstrating event-based interrupt handling.
    The program continues running while PIR sensor events are handled asynchronously.
    """
    global motion_count
    
    try:
        print("=" * 60)
        print("PIR Sensor - Event-Based Interrupt Mode (gpiozero)")
        print("=" * 60)
        print("PIR Sensor initialized on GPIO 4")
        print("Waiting for motion events...")
        print("Press Ctrl+C to stop\n")
        
        # Attach callback functions to PIR sensor events
        pir.when_motion = on_motion
        pir.when_no_motion = on_no_motion
        
        # Main loop continues here while PIR events are handled in background
        cycle = 0
        while True:
            cycle += 1
            
            # Example: Main program can perform other tasks
            print(f"[MAIN] Cycle #{cycle} - Status: {get_motion_status()} | Total events: {motion_count}")
            
            # Simulate other robot tasks
            sleep(2)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Program stopped by user")
        print(f"Total motion events detected: {motion_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Cleanup GPIO resources
        pir.close()
        print("PIR sensor cleanup completed")


if __name__ == '__main__':
    main()
