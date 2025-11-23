"""
Author      : KOH KHENG CHOONG
Date        : 2025-11-09
Description : This is a python code for Raspberry Pi 3B to integrate multiple sensors (IR, Ultrasonic, PIR) and LED for a surveillance robot application.
            : Task 1 (motion control)
            : - using 2 LEDs to represent the Motion control
            - forward movement = left and right LED are lit(LED_left = 17 and LED_right = 27)
            - backward movement = left and right LED are blinking at rate of 100ms
            - right turn = right LED will blink at rate of 10ms
            - left turn = left LED will blink at rate of 10ms
            - stop = both LED off
            : Task 2 (obstacle detection)
            : - using ultrasonic sensor to detect obstacle within 20cm distance
            - i. first , the robot will stop and turn the sensor(left to right using SG90 srvo) to scan the surronding area to find a new sroute to proceed
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
from gpiozero import LED, MCP3008, MotionSensor, DistanceSensor,PWMOutputDevice
from gpiozero.pins.pigpio import PiGPIOFactory
import pigpio
from time import sleep
import time


battery_low_threshold = 3.0  # example threshold for low battery

# Configuration
OBSTACLE_THRESHOLD_CM = 16
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
spotlight = LED(5)
obstacle_alert_led = LED(6)
pir = MotionSensor(4, queue_len =1, sample_rate = 10, threshold =0.5)    # GPIO4
v_regulation = MCP3008(0)  # assuming the sensor is connected to channel 0
buzzer = PWMOutputDevice(22, frequency = 440, initial_value =0)
ultrasonic_echo = 15
ultrasonic_trigger = 14
sensor = DistanceSensor(echo=ultrasonic_echo, trigger=ultrasonic_trigger,max_distance=4, pin_factory=PiGPIOFactory())

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
        sleep(0.1)
        return sensor.distance * 100  # convert to cm and sensor is 
    except Exception as e:
        print(f"Error reading distance: {e}")



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
    sleep(0.8)
    left_distance = get_distance_cm()
    left_obstacle = detect_obstacle(left_distance)
    results['left'] = left_obstacle
    results['left_distance'] = left_distance
    print(f"Distance: {left_distance:.2f} cm | Obstacle: {left_obstacle}")
    
    # Scan CENTER direction (90 degrees)
    print("\n[CENTER] Scanning at 90°...")
    set_angle(ANGLE_CENTER)
    sleep(0.8)
    center_distance = get_distance_cm()
    center_obstacle = detect_obstacle(center_distance)
    results['center'] = center_obstacle
    results['center_distance'] = center_distance
    print(f"Distance: {center_distance:.2f} cm | Obstacle: {center_obstacle}")
    
    # Scan RIGHT direction (135 degrees)
    print("\n[RIGHT] Scanning at 135°...")
    set_angle(ANGLE_RIGHT)
    sleep(0.8)
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
    spotlight.on()
    # Sound alarm - buzzer + LED flash
    for _ in range(5):
        buzzer.value = 0.7      
        sleep(0.3)
        
        buzzer.value = 0       
        sleep(0.3)
    
    buzzer.value = 0
 
    print("[ALARM] Intruder alarm deactivated\n")



def on_no_motion():
    """
    Callback function triggered when motion stops.
    """
    global last_motion_event, alarm_active
    last_motion_event = "No Motion"
    alarm_active = False
    buzzer.value = 0
    spotlight.off()
    print(f"[INTERRUPT] No motion detected")
    print(f"Timestamp: {time.strftime('%H:%M:%S', time.localtime())}\n")



def get_motion_status():
    """
    Non-blocking function to get current motion status.
    Returns: True if motion detected, False otherwise
    """
    return pir.motion_detected


def obstacle_avoidance_logic(left_obs, center_obs, right_obs):
    """
    Obstacle avoidance decision logic based on sensor readings.
    
    Truth Table:
    Left | Center | Right | Action
    -----|--------|-------|-------------------
      0  |   0    |   0   | Forward
      0  |   0    |   1   | Forward
      0  |   1    |   0   | Turn Left
      0  |   1    |   1   | Turn Left
      1  |   0    |   0   | Forward
      1  |   0    |   1   | Forward
      1  |   1    |   0   | Turn Right
      1  |   1    |   1   | Backward + Turn Left
    
    Args:
        left_obs (bool): True if obstacle detected on LEFT
        center_obs (bool): True if obstacle detected on CENTER
        right_obs (bool): True if obstacle detected on RIGHT
    
    Returns:
        str: Action to take ("forward", "left", "right", "backward_left")
    """
    # Convert to binary values
    left = 1 if left_obs else 0
    center = 1 if center_obs else 0
    right = 1 if right_obs else 0
    
    # Apply truth table logic
    if left == 0 and center == 0 and right == 0:
        return "forward"  # 0 0 0
    elif left == 0 and center == 0 and right == 1:
        return "forward"  # 0 0 1
    elif left == 0 and center == 1 and right == 0:
        return "left"     # 0 1 0
    elif left == 0 and center == 1 and right == 1:
        return "left"     # 0 1 1
    elif left == 1 and center == 0 and right == 0:
        return "forward"  # 1 0 0
    elif left == 1 and center == 0 and right == 1:
        return "forward"  # 1 0 1
    elif left == 1 and center == 1 and right == 0:
        return "right"    # 1 1 0
    elif left == 1 and center == 1 and right == 1:
        return "backward_left"  # 1 1 1
    
    return "forward"  # Default action
 

def check_voltage_regulation(min_voltage=3.2):
    """
    Check voltage regulation/battery level from MCP3008 channel 0.
    
    MCP3008 returns a normalized value (0.0-1.0) representing 0V to 3.3V.
    If a voltage divider is used, multiply by voltage_divider to get actual battery voltage.
    
    Args:
        min_voltage (float): Minimum safe voltage threshold in volts.
        voltage_divider (float): Voltage divider ratio (default 3.0 for 2S LiPo ~7.4V).
    
    Returns:
        bool: True if voltage is OK or exceeds min_voltage; False if below threshold.
    """
    try:
        # v_regulation is MCP3008(0) - reads normalized value 0.0-1.0
        adc_value = v_regulation.value
        # Convert to actual voltage: ADC reads 0V-3.3V at Pi reference
        # If voltage divider is used, scale by divider ratio
        actual_voltage = adc_value * 3.3 
        print(f"[VOLTAGE] ADC: {adc_value:.3f} → {actual_voltage:.2f}V (min {min_voltage}V)")
        return actual_voltage >= min_voltage
    except Exception as e:
        print(f"[VOLTAGE] Voltage check error: {e}")
        return True  # Safe default: allow movement on error


def patrol_logic():
    """
    Patrol logic following the flowchart:
    - Triggered by motion interrupt state (motion flag managed elsewhere)
    - Check voltage regulation first
    - If movement_counter < MOVEMENT_COUNTER_LIMIT: scan and move according to truth table
    - If movement_counter >= MOVEMENT_COUNTER_LIMIT: check RIGHT obstacle before turning right
    """
    global movement_counter, patrol_active

    print("\n" + "=" * 70)
    print("PATROL LOGIC STARTED - Flowchart-driven with Voltage Check")
    print("=" * 70)

    while patrol_active:
        # Motion interrupt triggers are handled by on_motion(); here we run looped patrol
        print(f"\n[STATE] Movement counter: {movement_counter} / {MOVEMENT_COUNTER_LIMIT}")

        # Voltage regulation check
        if not check_voltage_regulation():
            print("[VOLTAGE] Voltage too low - entering idle/charging mode")
            stop()
            sleep(2)
            continue

        if movement_counter < MOVEMENT_COUNTER_LIMIT:
            # Scan for obstacles and decide
            print(f"[SCAN] Scanning obstacles BEFORE movement {movement_counter + 1}/{MOVEMENT_COUNTER_LIMIT}...")
            scan_results = scan_obstacles()
            left_obstacle = scan_results['left']
            center_obstacle = scan_results['center']
            right_obstacle = scan_results['right']

            action = obstacle_avoidance_logic(left_obstacle, center_obstacle, right_obstacle)
            print(f"[LOGIC] LEFT:{left_obstacle} CENTER:{center_obstacle} RIGHT:{right_obstacle} → {action}")

            if action == 'forward':
                print(f"[MOVE] Forward movement {movement_counter + 1}/{MOVEMENT_COUNTER_LIMIT}")
                forward()
                sleep(2)
                stop()
                movement_counter += 1
            elif action == 'left':
                print("[AVOID] Turning LEFT to avoid obstacle")
                #when obstacle detected ,obstacle_led will blink at 1s interval
                obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                left_turn()
            elif action == 'right':
                print("[AVOID] Turning RIGHT to avoid obstacle")
                #when obstacle detected ,obstacle_led will blink at 1s interval
                obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                right_turn()
            elif action == 'backward_left':
                print("[AVOID] All blocked - moving BACKWARD then LEFT")
                #when obstacle detected ,obstacle_led will blink at 1s interval
                obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                backward()
                left_turn()
                movement_counter = 0

        else:
            # movement_counter reached limit; before turning right, check right obstacle
            print("[CHECK] Reached movement limit - checking RIGHT before turning")
            scan_results = scan_obstacles()
            if scan_results['right']:
                print("[CHECK] RIGHT is blocked - running avoidance logic")
                # Use full obstacle avoidance based on current scan
                action = obstacle_avoidance_logic(scan_results['left'], scan_results['center'], scan_results['right'])
                if action == 'forward':
                    #when obstacle detected ,obstacle_led will blink at 1s interval
                    obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                    forward(); sleep(2); stop(); movement_counter += 1
                elif action == 'left':
                    #when obstacle detected ,obstacle_led will blink at 1s interval
                    obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                    left_turn()
                elif action == 'right':
                    #when obstacle detected ,obstacle_led will blink at 1s interval
                    obstacle_alert_led.blink(on_time=1, off_time=1, n=5)
                    right_turn()
                elif action == 'backward_left':
                    backward(); left_turn(); movement_counter = 0
            else:
                print("[TURN] RIGHT is clear - perform corner turn (right)")
                right_turn()
                movement_counter = 0

        sleep(0.5)


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