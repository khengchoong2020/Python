"""
Author      : KOH KHENG CHOONG
Date        : 2025-11-09
Description : This is a python code for Raspberry Pi 3B to integrate multiple sensors (IR, Ultrasonic, PIR) and an LED for a surveillance robot application.
            : Task 1 (motion control)
            : - using 2 LEDs to represent the Motion control
            - forward movement = left and right LED are lit(LED_left = 17 and LED_right = 23)
            - backward movement = left and right LED are blinking at rate of 100ms
            - right turn = right LED will blink at rate of 10ms
            - left turn = left LED will blink at rate of 10ms
            - stop = both LED off
            : Task 2 (obstacle detection)
            : - using ultrasonic sensor to detect obstacle within 20cm distance
            - i. first , the robot will stop and turn the sensor(left to right using SG90 srvo) to scan the surronding area ti find a new sroute to proceed
            - ii reverse and turn slightly left or right and seume patrol logic from adjusted position
            : Task 3 (alarm system)
            - obstacle avoidance alert blinking LEDs at a rate of 1s
            - intruder alert using PIR = Buzzer sound
            - low battery level alerrt = blinking and buzzer soung
            -task 4 (power management)
            I maintain a stable DC power supply for the circuits
            II Fuse and polarity reverse protection
            III monitor the voltatge lvel of the battery using MCP3008 ADC
            IV to alarrt the user to charge the battery
            V safety switch to manual overrides the system

            task 5 (motion detection)
            turn on the spotlight , actiuvate the intruder alert


            buzzer = GPIO22
            ultrasonic echo = 15 trigger = 14
            LED_left = 17
            LED_right = 23
            motion sensor = 4
            SG90 = 18
            MCP3008 = channel 0 for IR sensor and channel 1 for battery level detection channel 2 for voltage monitor

"""
# Import necessary libraries
from gpiozero import LED, MCP3008, MotionSensor, DistanceSensor,PWMOutputDevice,Button
from gpiozero.pins.pigpio import PiGPIOFactory
import pigpio
from time import sleep
import time

#battery_voltage_divider = 3.0
#battery_low_threshold = 6.5  # example threshold for low battery
#battery_reference_voltage = 3.3

#obstacle_distance_threshold = 20  # in cm

#intruder_alert_colddown = 30
#low_battery_alert_cooldown = 60

#servo_center_angle = 90
#servo_scan_angles = range(0, 181, 30)

#emergency_stop_pin = 23  # GPIO pin for emergency stop switch

# Configuration
OBSTACLE_THRESHOLD_CM = 20
MOVEMENT_COUNTER_LIMIT = 5
INTRUDER_ALERT_COOLDOWN = 30

# Scan angles
ANGLE_LEFT = 180      # Left direction
ANGLE_CENTER = 90    # Center direction
ANGLE_RIGHT = 0    # Right direction

# GPIO Initialization 
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")
# GPIO pin for servo
SERVO_PIN = 18
LEDLeft = LED(17)
LEDRight = LED(27)
pir = MotionSensor(4, queue_len =1, sample_rate = 10, threshold =0.5)    # GPIO4
v_regulation = MCP3008(0)  # assuming the sensor is connected to channel 0
#battery_level_sensor = MCP3008(1)  # channel 1 for battery level detection
#voltage_monitor_sensor = MCP3008(2)  # channel 2 for voltage monitoring
buzzer = PWMOutputDevice(22, frequency = 440, initial_value =0)
ultrasonic_echo = 15
ultrasonic_trigger = 14
sensor = DistanceSensor(echo=ultrasonic_echo, trigger=ultrasonic_trigger,max_distance=4, pin_factory=PiGPIOFactory())

#emergency_stop = Button(emergency_stop_pin, pull_up=True, bounce_time=0.1)
system_active = True

#last_intruder_alert = 0
#last_battery_alert = 0
#servo_angle = servo_center_angle

# Global state tracking
motion_detected_time = 0
motion_count = 0
last_motion_event = None
alarm_active = False

movement_counter = 0
patrol_active = False

# Functions
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

def stop_servo():
    pi.set_servo_pulsewidth(SERVO_PIN, 0)

def get_distance_cm():
    try:
        return sensor.distance * 100  # convert to cm and sensor is ultrasonic
    except Exception as e:
        print(f"Error reading distance: {e}")

#def get_battery_voltage():
#    adc_value = battery_level_sensor.value  # MCP3008 value between 0 and 1
#    voltage = adc_value * battery_reference_voltage * battery_voltage_divider
#    return voltage

#def check_emergency_stop():    
#    global system_active
#    if not emergency_stop.is_pressed:
#        system_active = False
#        print("Emergency stop activated! Shutting down the system.")
#        stop_all()
#    return False

def detect_obstacle(distance):
    """
    Determine if obstacle is detected based on distance threshold.
    
    Args:
        distance: Distance in cm
    
    Returns:
        bool: True if obstacle detected (distance < 20cm), False otherwise
    """
    return distance < OBSTACLE_THRESHOLD_CM


def scan_obstacles():
    """
    Scan three directions (left, center, right) and detect obstacles.
    
    Returns:
        dict: Contains obstacle detection results
            - 'left': bool (True if obstacle detected at 45°)
            - 'center': bool (True if obstacle detected at 90°)
            - 'right': bool (True if obstacle detected at 135°)
            - 'left_distance': float (distance in cm)
            - 'center_distance': float (distance in cm)
            - 'right_distance': float (distance in cm)
    """
    print("=" * 60)
    print("Scanning for obstacles...")
    print("=" * 60)
    
    results = {}
    
    # Scan LEFT direction (45 degrees)
    print("\n[LEFT] Scanning at 45°...")
    set_angle(ANGLE_LEFT)
    sleep(0.5)
    left_distance = get_distance_cm()
    left_obstacle = detect_obstacle(left_distance)
    results['left'] = left_obstacle
    results['left_distance'] = left_distance
    print(f"Distance: {left_distance:.2f} cm | Obstacle: {left_obstacle}")
    
    # Scan CENTER direction (90 degrees)
    print("\n[CENTER] Scanning at 90°...")
    set_angle(ANGLE_CENTER)
    sleep(0.5)
    center_distance = get_distance_cm()
    center_obstacle = detect_obstacle(center_distance)
    results['center'] = center_obstacle
    results['center_distance'] = center_distance
    print(f"Distance: {center_distance:.2f} cm | Obstacle: {center_obstacle}")
    
    # Scan RIGHT direction (135 degrees)
    print("\n[RIGHT] Scanning at 135°...")
    set_angle(ANGLE_RIGHT)
    sleep(0.5)
    right_distance = get_distance_cm()
    right_obstacle = detect_obstacle(right_distance)
    results['right'] = right_obstacle
    results['right_distance'] = right_distance
    print(f"Distance: {right_distance:.2f} cm | Obstacle: {right_obstacle}")
    
    # Return servo to center
    set_angle(ANGLE_CENTER)
    sleep(0.5)
    stop_servo()
    sleep(0.5)
    
    return results


def report_obstacles(results):
    """
    Print formatted obstacle detection report.
    
    Args:
        results: Dictionary returned from scan_obstacles()
    """
    print("\n" + "=" * 60)
    print("OBSTACLE DETECTION REPORT")
    print("=" * 60)
    print(f"LEFT (45°)    : {results['left']:5} | Distance: {results['left_distance']:6.2f} cm")
    print(f"CENTER (90°)  : {results['center']:5} | Distance: {results['center_distance']:6.2f} cm")
    print(f"RIGHT (135°)  : {results['right']:5} | Distance: {results['right_distance']:6.2f} cm")
    print("=" * 60)
    
    # Determine best direction to move
    if not results['center']:
        print("✓ CENTER is clear - Safe to move forward")
    elif not results['left']:
        print("✓ LEFT is clear - Turn left to avoid obstacles")
    elif not results['right']:
        print("✓ RIGHT is clear - Turn right to avoid obstacles")
    else:
        print("✗ All directions blocked - Reverse and try again")
    print()

def stop_all():
    LEDLeft.off()
    LEDRight.off()
    stop_servo()
    buzzer.value = 0
    pi.stop()

def LED_BLINK(count, interval, left=True, right=True):
    for _ in range(count):
#        if check_emergency_stop():
#            return
        if left:
            LEDLeft.toggle()            
        if right:
            LEDRight.toggle()
        sleep(interval)
    
    if left:
        LEDLeft.off()
    if right:
        LEDRight.off()

def forward():
  LEDLeft.on()
  LEDRight.on()

def backward():
  # Both LEDs blink at 100ms for 2 seconds
  LED_BLINK(count =20, interval = 0.1, left = True, right = True)
  sleep(1)
  LEDLeft.off()
  LEDRight.off()  

def right_turn():
  LED_BLINK(count =20, interval = 0.1, left = False, right = True)
  sleep(1)
  LEDLeft.off()
  LEDRight.off()  
  

def left_turn():
  LED_BLINK(count =20, interval = 0.1, left = True, right = False)
  sleep(1)
  LEDLeft.off()
  LEDRight.off()  

def stop():
  LEDLeft.off()
  LEDRight.off()  

def on_motion():
    """
    Callback function triggered when motion is detected.
    Activates intruder alarm with buzzer and LED flashing.
    """
    global motion_detected_time, motion_count, last_motion_event, alarm_active
    motion_detected_time = time.time()
    motion_count += 1
    last_motion_event = "Motion"
    alarm_active = True
    print(f"\n[ALARM] Motion detected! (Event #{motion_count})")
    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime(motion_detected_time))}")
    
    # Sound alarm - buzzer + LED flash
    for _ in range(5):
        buzzer.value = 0.7
        LEDLeft.on()
        LEDRight.on()
        sleep(0.3)
        
        buzzer.value = 0
        LEDLeft.toggle()
        LEDRight.toggle()
        sleep(0.3)
    
    buzzer.value = 0
    LEDLeft.off()
    LEDRight.off()
    print("[ALARM] Intruder alarm deactivated\n")



def on_no_motion():
    """
    Callback function triggered when motion stops.
    """
    global last_motion_event, alarm_active
    last_motion_event = "No Motion"
    alarm_active = False
    buzzer.value = 0
    LEDLeft.off()
    LEDRight.off()
    print(f"[INTERRUPT] No motion detected")
    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime())}\n")



def get_motion_status():
    """
    Non-blocking function to get current motion status.
    Returns: True if motion detected, False otherwise
    """
    return pir.motion_detected


def patrol_logic():
    """
    Patrol logic with obstacle detection BEFORE movement:
    - Scan for obstacles before each movement
    - Move forward in counter of 5 (each iteration 2 seconds)
    - After 5th iteration: turn right and reset counter
    - Repeat continuously
    """
    global movement_counter, patrol_active
    
    print("\n" + "=" * 70)
    print("PATROL LOGIC STARTED - Square Pattern with Pre-Movement Obstacle Detection")
    print("=" * 70)
    print("Pattern: Scan obstacles → Move forward (2 sec) → x5 → Turn Right → Repeat\n")
    
    while patrol_active:
        # STEP 1: Scan for obstacles BEFORE movement
        print(f"\n[SCAN] Scanning obstacles BEFORE movement {movement_counter + 1}/5...")
        scan_results = scan_obstacles()
        
        # Check if center is clear to proceed
        if scan_results['center']:
            print("⚠ WARNING: CENTER direction has obstacle - cannot proceed safely!")
            print("Checking alternate routes...")
            
            if not scan_results['left']:
                print("✓ LEFT is clear - Turning left instead...")
                left_turn()
            elif not scan_results['right']:
                print("✓ RIGHT is clear - Turning right instead...")
                right_turn()
            else:
                print("✗ All directions blocked! Stopping patrol...")
                stop()
                break
        else:
            print("✓ CENTER is clear - Safe to move forward")
            
            # STEP 2: Move forward for 2 seconds
            print(f"[MOVE] Forward movement {movement_counter + 1}/5")
            forward()
            sleep(2)
            stop()
            
            # Increment counter
            movement_counter += 1
            
            # STEP 3: Check if reached 5 iterations
            if movement_counter >= MOVEMENT_COUNTER_LIMIT:
                print(f"\n[TURN] Completed 5 forward movements - Turning right...\n")
                right_turn()
                movement_counter = 0  # Reset counter
        
        sleep(0.5)



#    print("Obstacle detected! Initiating avoidance maneuvers.")
#    # Stop movement
#    LEDLeft.off()
#    LEDRight.off()
#    sleep(1)

    # Scan surroundings
#    for angle in range(0, 181, 30):
#        set_angle(angle)
#        sleep(0.5)
#        distance = sensor.distance * 100  # convert to cm
#        print(f"Angle: {angle}, Distance: {distance:.2f} cm")
#        if distance > 20:
#            print("Clear path found!")
#            break

    # Reverse and turn slightly
#    for _ in range(5):
#        LEDLeft.toggle()
#        LEDRight.toggle()
#        sleep(0.1)
#    LEDLeft.on()
#    sleep(1)

#def intruder_alert():
#    print("Intruder detected! Activating alarm.")
#    for _ in range(5):
#        buzzer.value = 0.5
#        LEDLeft.toggle()
#        LEDRight.toggle()
#        sleep(0.5)
#        buzzer.value = 0
#        sleep(0.5)

#def low_battery_alert():
#    print("Low battery level! Activating alert.")
#    for _ in range(5):
#        buzzer.value = 0.5
#        LEDLeft.toggle()
#        LEDRight.toggle()
#        sleep(0.5)
#        buzzer.value = 0
#        sleep(0.5)

def main():
    """Main program loop for surveillance robot patrol."""
    global motion_count, patrol_active

    # Attach callback functions to PIR sensor events
    pir.when_motion = on_motion
    pir.when_no_motion = on_no_motion

    try:
        print("\n" + "=" * 70)
        print("SURVEILLANCE ROBOT - Simple Square Patrol")
        print("=" * 70)
        print("\nFEATURES:")
        print("  • Forward movement with counter (5 iterations)")
        print("  • 2 seconds per forward movement")
        print("  • Right turn after every 5 movements")
        print("  • LED indicators for movement")
        print("  • PIR motion sensor with intruder alarm")
        print("\nLED INDICATORS:")
        print("  • Forward: Both LEDs ON")
        print("  • Turn Right: Right LED blinks")
        print("  • Stop: Both LEDs OFF")
        print("\nPress Ctrl+C to stop\n")
        
        patrol_active = True
        
        # Start patrol
        patrol_logic()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Program stopped by user")
        print(f"Total motion events: {motion_count}")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        patrol_active = False
        stop()
        buzzer.value = 0
        set_angle(90)
        time.sleep(0.3)
        stop_servo()
        pir.close()
        pi.stop()
        print("Cleanup completed")

if __name__ == '__main__':
    main()