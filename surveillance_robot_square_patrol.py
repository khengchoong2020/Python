'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-16
Description = Surveillance Robot Patrol in Square Pattern with Obstacle Detection
            = Features:
            = 1. Scans for obstacles in 3 directions (LEFT 45°, CENTER 90°, RIGHT 135°)
            = 2. Moves forward with counter (5 steps)
            = 3. Turns right when counter reaches 5
            = 4. Checks for obstacles after each turn
            = 5. Adjusts direction if obstacle detected
            = 6. PIR sensor with callback for intruder alarm
            = 7. LED indicators for movement direction
'''

from gpiozero import LED, MotionSensor, DistanceSensor, PWMOutputDevice
import pigpio
from time import sleep
import time

# ============================================================================
# GPIO CONFIGURATION
# ============================================================================
# LEDs
LED_LEFT = LED(17)
LED_RIGHT = LED(23)

# Buzzer (for intruder alarm)
buzzer = PWMOutputDevice(22, frequency=440, initial_value=0)

# PIR Motion Sensor
pir = MotionSensor(4, queue_len=1, sample_rate=10, threshold=0.5)

# Ultrasonic Distance Sensor
ultrasonic = DistanceSensor(echo=15, trigger=14)

# Servo (SG90) for obstacle scanning
SERVO_PIN = 18
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")

# ============================================================================
# CONFIGURATION
# ============================================================================
OBSTACLE_THRESHOLD_CM = 20
SERVO_CENTER = 90
SERVO_LEFT = 45
SERVO_RIGHT = 135

MOVEMENT_COUNTER_LIMIT = 5
INTRUDER_ALERT_COOLDOWN = 30

# ============================================================================
# STATE TRACKING
# ============================================================================
patrol_active = False
movement_counter = 0
square_count = 0
last_intruder_alert = 0
alarm_active = False

# Obstacle detection results
left_obstacle = False
center_obstacle = False
right_obstacle = False


# ============================================================================
# SERVO CONTROL FUNCTIONS
# ============================================================================

def set_angle(angle):
    """Set servo angle (0-180 degrees)."""
    if not 0 <= angle <= 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    pulse_width = int(500 + (angle * 2000 / 180))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)


def stop_servo():
    """Stop servo pulses."""
    pi.set_servo_pulsewidth(SERVO_PIN, 0)


# ============================================================================
# DISTANCE SENSOR FUNCTIONS
# ============================================================================

def get_distance_cm():
    """Get distance from ultrasonic sensor in cm."""
    try:
        return ultrasonic.distance * 100
    except:
        return 999


def detect_obstacle(distance):
    """Check if obstacle detected (distance < 20cm)."""
    return distance < OBSTACLE_THRESHOLD_CM


# ============================================================================
# OBSTACLE SCANNING FUNCTION
# ============================================================================

def scan_obstacles():
    """
    Scan 3 directions for obstacles.
    
    Updates global variables:
        - left_obstacle (bool)
        - center_obstacle (bool)
        - right_obstacle (bool)
    
    Returns:
        dict with scan results
    """
    global left_obstacle, center_obstacle, right_obstacle
    
    print("\n[SCAN] Scanning for obstacles...")
    
    # LEFT direction (45°)
    set_angle(SERVO_LEFT)
    sleep(0.3)
    left_distance = get_distance_cm()
    left_obstacle = detect_obstacle(left_distance)
    print(f"  LEFT (45°):   {left_distance:.1f} cm | Obstacle: {left_obstacle}")
    
    # CENTER direction (90°)
    set_angle(SERVO_CENTER)
    sleep(0.3)
    center_distance = get_distance_cm()
    center_obstacle = detect_obstacle(center_distance)
    print(f"  CENTER (90°): {center_distance:.1f} cm | Obstacle: {center_obstacle}")
    
    # RIGHT direction (135°)
    set_angle(SERVO_RIGHT)
    sleep(0.3)
    right_distance = get_distance_cm()
    right_obstacle = detect_obstacle(right_distance)
    print(f"  RIGHT (135°): {right_distance:.1f} cm | Obstacle: {right_obstacle}")
    
    # Return servo to center
    set_angle(SERVO_CENTER)
    stop_servo()
    
    return {
        'left': left_obstacle,
        'center': center_obstacle,
        'right': right_obstacle,
        'left_distance': left_distance,
        'center_distance': center_distance,
        'right_distance': right_distance
    }


# ============================================================================
# MOVEMENT FUNCTIONS
# ============================================================================

def move_forward():
    """Move forward - both LEDs ON."""
    print("[MOVE] Moving forward...")
    LED_LEFT.on()
    LED_RIGHT.on()
    sleep(0.5)


def turn_right():
    """Turn right - right LED blinks."""
    print("[TURN] Turning right...")
    LED_LEFT.off()
    
    # Blink right LED
    for _ in range(10):
        LED_RIGHT.toggle()
        sleep(0.01)
    
    LED_RIGHT.off()
    sleep(0.3)


def turn_left():
    """Turn left - left LED blinks."""
    print("[TURN] Turning left...")
    LED_RIGHT.off()
    
    # Blink left LED
    for _ in range(10):
        LED_LEFT.toggle()
        sleep(0.01)
    
    LED_LEFT.off()
    sleep(0.3)


def stop_movement():
    """Stop - both LEDs OFF."""
    print("[STOP] Stopping...")
    LED_LEFT.off()
    LED_RIGHT.off()


# ============================================================================
# INTRUDER ALARM CALLBACK
# ============================================================================

def on_motion():
    """
    Callback triggered when motion detected by PIR sensor.
    Activates intruder alarm with buzzer and LED flashing.
    """
    global last_intruder_alert, alarm_active
    
    current_time = time.time()
    if current_time - last_intruder_alert >= INTRUDER_ALERT_COOLDOWN:
        alarm_active = True
        last_intruder_alert = current_time
        print("\n[ALARM] *** INTRUDER DETECTED! ***")
        trigger_intruder_alarm()


def on_no_motion():
    """Callback triggered when motion stops."""
    global alarm_active
    alarm_active = False
    buzzer.value = 0
    LED_LEFT.off()
    LED_RIGHT.off()


def trigger_intruder_alarm(flash_count=5):
    """Sound alarm with buzzer and LED flashing."""
    print("[ALARM] Sounding alarm...")
    
    for _ in range(flash_count):
        if not alarm_active:
            break
        buzzer.value = 0.7
        LED_LEFT.on()
        LED_RIGHT.on()
        sleep(0.3)
        
        buzzer.value = 0
        LED_LEFT.toggle()
        LED_RIGHT.toggle()
        sleep(0.3)
    
    buzzer.value = 0
    LED_LEFT.off()
    LED_RIGHT.off()
    print("[ALARM] Alarm deactivated")


# ============================================================================
# PATROL LOGIC - MAIN ALGORITHM
# ============================================================================

def patrol_with_obstacle_avoidance():
    """
    Main patrol loop:
    1. Scan obstacles in 3 directions
    2. Move forward (counter = 0)
    3. Increment counter
    4. At EACH counter increment: Check obstacles
    5. If counter == 5: Turn right, reset counter
    6. Repeat
    """
    global movement_counter, patrol_active, square_count
    
    print("\n" + "=" * 70)
    print("PATROL START - Square Pattern with Obstacle Detection")
    print("=" * 70 + "\n")
    
    # Initial obstacle scan
    scan_results = scan_obstacles()
    
    # Check if center is clear to proceed
    if scan_results['center']:
        print("⚠ Center has obstacle! Attempting to find alternate route...")
        
        if not scan_results['left']:
            print("✓ LEFT is clear - Turning left...")
            turn_left()
        elif not scan_results['right']:
            print("✓ RIGHT is clear - Turning right...")
            turn_right()
        else:
            print("✗ All directions blocked! Stopping patrol...")
            stop_movement()
            return False
    
    movement_counter = 0
    
    # Main patrol loop
    while patrol_active:
        # STEP 1: Check for intruder (non-blocking)
        if alarm_active:
            print("⚠ Alarm active - Continuing patrol...")
        
        # STEP 2: Move forward
        move_forward()
        movement_counter += 1
        
        print(f"[COUNTER] Movement: {movement_counter}/{MOVEMENT_COUNTER_LIMIT}")
        
        # STEP 3: OBSTACLE CHECK AT EVERY COUNTER INCREMENT
        print("\n[SCAN] Checking obstacles at counter increment...")
        scan_results = scan_obstacles()
        
        # Determine next action based on obstacle detection
        if scan_results['center']:
            print("⚠ CENTER has obstacle! Need to adjust...")
            
            if not scan_results['left']:
                print("✓ LEFT is clear - Turning left...")
                turn_left()
            elif not scan_results['right']:
                print("✓ RIGHT is clear - Turning right...")
                turn_right()
            else:
                print("✗ All directions blocked! Stopping patrol...")
                stop_movement()
                break
        else:
            print("✓ CENTER is clear - Safe to continue")
        
        # STEP 4: Check if counter reached limit (5 movements)
        if movement_counter >= MOVEMENT_COUNTER_LIMIT:
            print(f"\n[COUNTER] Reached limit ({MOVEMENT_COUNTER_LIMIT}) - Preparing to turn right...")
            movement_counter = 0
            square_count += 1
            
            # Turn right at corner
            turn_right()
            print(f"[SQUARE] Completed corner turn #{square_count}\n")
        
        sleep(0.5)
    
    return True


# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program loop."""
    global patrol_active
    
    try:
        print("\n" + "=" * 70)
        print("SURVEILLANCE ROBOT PATROL - Square Pattern")
        print("=" * 70)
        print("\nFEATURES:")
        print("  • Obstacle scanning in 3 directions (LEFT, CENTER, RIGHT)")
        print("  • Movement counter (5 steps before turning)")
        print("  • Automatic obstacle avoidance")
        print("  • Intruder detection with alarm callback")
        print("  • LED indicators for movement direction")
        print("\nLED INDICATORS:")
        print("  • Forward: Both LEDs ON")
        print("  • Turn: LEDs blink")
        print("  • Stop: Both LEDs OFF")
        print("\nPIR SENSOR: Motion detection triggers intruder alarm")
        print("Press Ctrl+C to stop\n")
        
        # Attach PIR callbacks
        pir.when_motion = on_motion
        pir.when_no_motion = on_no_motion
        
        patrol_active = True
        
        # Start patrol
        patrol_with_obstacle_avoidance()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Program stopped by user")
        print(f"Completed squares: {square_count}")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Cleanup
        print("\nCleaning up...")
        patrol_active = False
        stop_movement()
        buzzer.value = 0
        set_angle(SERVO_CENTER)
        sleep(0.3)
        stop_servo()
        pir.close()
        pi.stop()
        print("Cleanup completed")


if __name__ == '__main__':
    main()
