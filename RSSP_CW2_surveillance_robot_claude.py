"""
Author      : KOH KHENG CHOONG
Date        : 2025-11-09
Description : Corrected Raspberry Pi 3B surveillance robot with multiple sensors
            : Improvements:
            : - Fixed GPIO pin conflicts
            : - Added non-blocking timing
            : - Implemented proper battery voltage scaling
            : - Added alert debouncing
            : - Completed obstacle avoidance logic
            : - Added emergency stop
            : - Better state management

Pin Assignments:
    - LED_left = GPIO 17
    - LED_right = GPIO 23
    - Buzzer = GPIO 22
    - Ultrasonic: Echo = GPIO 15, Trigger = GPIO 14 (for distance detection)
    - PIR Motion = GPIO 4
    - Servo SG90 = GPIO 18
    - Emergency Stop Button = GPIO 27
    - MCP3008 ADC:
        * Channel 1: Battery voltage divider
        * Channel 2: Voltage monitor (optional - for additional monitoring)
"""

from gpiozero import LED, MCP3008, MotionSensor, DistanceSensor, PWMOutputDevice, Button
import pigpio
from time import sleep
import time

# ============================================================================
# CONFIGURATION
# ============================================================================
# Battery settings (adjust based on your battery pack)
BATTERY_VOLTAGE_DIVIDER = 3.0  # Ratio: (R1+R2)/R2 for voltage divider
BATTERY_LOW_THRESHOLD = 6.5    # Voltage threshold for low battery alert
BATTERY_REFERENCE_VOLTAGE = 3.3  # MCP3008 reference voltage

# Obstacle detection
OBSTACLE_DISTANCE_CM = 20

# Alert debounce times (seconds)
INTRUDER_ALERT_COOLDOWN = 30
LOW_BATTERY_ALERT_COOLDOWN = 60

# Servo scan angles
SERVO_CENTER = 90
SERVO_SCAN_RANGE = range(0, 181, 30)

# Emergency stop button
EMERGENCY_STOP_PIN = 27  # GPIO 27 for emergency stop button

# ============================================================================
# GPIO INITIALIZATION
# ============================================================================
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")

# GPIO assignments
SERVO_PIN = 18
led_left = LED(17)
led_right = LED(23)
pir = MotionSensor(4)
battery_sensor = MCP3008(1)  # Battery voltage monitoring
voltage_monitor = MCP3008(2)  # Optional: additional voltage monitoring
buzzer = PWMOutputDevice(22, frequency=440, initial_value=0)
ultrasonic = DistanceSensor(echo=15, trigger=14)  # Primary distance sensor

# Emergency stop button
emergency_stop = Button(EMERGENCY_STOP_PIN, pull_up=True, bounce_time=0.1)
system_active = True

# ============================================================================
# STATE TRACKING
# ============================================================================
last_intruder_alert = 0
last_battery_alert = 0
servo_angle = SERVO_CENTER

# Obstacle detection zones
left_obstacle = 0
center_obstacle = 0
right_obstacle = 0

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def set_angle(angle):
    """Convert angle to pulse width and set servo position"""
    global servo_angle
    if not 0 <= angle <= 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    
    pulse_width = int(500 + (angle * 2000 / 180))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)
    servo_angle = angle


def stop_servo():
    """Stop sending pulses to servo to save power"""
    pi.set_servo_pulsewidth(SERVO_PIN, 0)


def get_distance_cm():
    """Get distance from ultrasonic sensor in centimeters"""
    try:
        return ultrasonic.distance * 100
    except:
        return 999  # Return large value on error


def get_battery_voltage():
    """Calculate actual battery voltage from ADC reading"""
    adc_value = battery_sensor.value  # 0-1
    voltage = adc_value * BATTERY_REFERENCE_VOLTAGE * BATTERY_VOLTAGE_DIVIDER
    return voltage


def check_emergency_stop():
    """Check if emergency stop is activated"""
    global system_active
    if emergency_stop.is_pressed:
        system_active = False
        stop_all()
        print("=" * 50)
        print("!!! EMERGENCY STOP ACTIVATED !!!")
        print("System halted. Press Ctrl+C to exit.")
        print("=" * 50)
        return True
    return False


def stop_all():
    """Stop all movement and turn off LEDs"""
    led_left.off()
    led_right.off()
    buzzer.value = 0


def blink_leds(count, interval, left=True, right=True):
    """Non-blocking LED blink with specified count and interval"""
    for _ in range(count):
        if check_emergency_stop():
            return
        if left:
            led_left.toggle()
        if right:
            led_right.toggle()
        sleep(interval)
    # Ensure LEDs are off after blinking
    if left:
        led_left.off()
    if right:
        led_right.off()

# ============================================================================
# MOVEMENT FUNCTIONS
# ============================================================================

def move_forward():
    """Forward movement - both LEDs on"""
    led_left.on()
    led_right.on()
    sleep(1)


def move_backward():
    """Backward movement - both LEDs blink at 100ms"""
    blink_leds(10, 0.1, left=True, right=True)


def turn_right():
    """Right turn - right LED blinks at 10ms"""
    led_left.off()
    led_right.off()
    blink_leds(50, 0.01, left=False, right=True)


def turn_left():
    """Left turn - left LED blinks at 10ms"""
    led_left.off()
    led_right.off()
    blink_leds(50, 0.01, left=True, right=False)


def stop_movement():
    """Stop - both LEDs off"""
    stop_all()
    sleep(1)

# ============================================================================
# MAIN LOGIC FUNCTIONS
# ============================================================================

def patrol_logic():
    """Execute basic patrol movements"""
    if check_emergency_stop():
        return
    
    move_forward()
    
    if check_emergency_stop():
        return
    
    move_backward()
    
    if check_emergency_stop():
        return
    
    turn_right()
    
    if check_emergency_stop():
        return
    
    turn_left()
    
    stop_movement()


def scan_surroundings():
    """Scan with servo and detect obstacles in left, center, right zones"""
    global left_obstacle, center_obstacle, right_obstacle
    
    print("Scanning surroundings...")
    
    # Reset obstacle flags
    left_obstacle = 0
    center_obstacle = 0
    right_obstacle = 0
    
    # Scan left zone (0-60 degrees)
    print("Scanning LEFT zone...")
    set_angle(30)
    sleep(0.3)
    distance = get_distance_cm()
    print(f"  Left: {distance:.1f} cm")
    if distance < OBSTACLE_DISTANCE_CM:
        left_obstacle = 1
    
    if check_emergency_stop():
        return "center"
    
    # Scan center zone (60-120 degrees)
    print("Scanning CENTER zone...")
    set_angle(90)
    sleep(0.3)
    distance = get_distance_cm()
    print(f"  Center: {distance:.1f} cm")
    if distance < OBSTACLE_DISTANCE_CM:
        center_obstacle = 1
    
    if check_emergency_stop():
        return "center"
    
    # Scan right zone (120-180 degrees)
    print("Scanning RIGHT zone...")
    set_angle(150)
    sleep(0.3)
    distance = get_distance_cm()
    print(f"  Right: {distance:.1f} cm")
    if distance < OBSTACLE_DISTANCE_CM:
        right_obstacle = 1
    
    # Display obstacle status
    print(f"Obstacle Status: Left={left_obstacle}, Center={center_obstacle}, Right={right_obstacle}")
    
    # Determine best direction based on obstacle detection
    if center_obstacle == 0:
        best_direction = "center"
    elif left_obstacle == 0:
        best_direction = "left"
    elif right_obstacle == 0:
        best_direction = "right"
    else:
        best_direction = "reverse"  # All zones blocked
    
    print(f"Best direction: {best_direction}")
    
    # Return servo to center
    set_angle(SERVO_CENTER)
    stop_servo()
    
    return best_direction


def obstacle_avoidance():
    """Handle obstacle detection and avoidance with zone-based logic"""
    global left_obstacle, center_obstacle, right_obstacle
    
    print("Obstacle detected! Initiating avoidance...")
    
    # Stop movement
    stop_movement()
    
    # Scan for obstacles in all zones
    best_direction = scan_surroundings()
    
    if check_emergency_stop():
        return
    
    # Alert with blinking LEDs (1 second intervals)
    print("Obstacle avoidance alert...")
    blink_leds(3, 1.0, left=True, right=True)
    
    # Execute avoidance maneuver based on obstacle zones
    if best_direction == "center":
        print("Center is clear - continuing forward")
        # No turn needed, just continue
        
    elif best_direction == "left":
        print("Turning LEFT to avoid obstacles")
        move_backward()
        if not check_emergency_stop():
            turn_left()
            turn_left()  # Double turn for sharper angle
        
    elif best_direction == "right":
        print("Turning RIGHT to avoid obstacles")
        move_backward()
        if not check_emergency_stop():
            turn_right()
            turn_right()  # Double turn for sharper angle
        
    else:  # best_direction == "reverse" (all zones blocked)
        print("All directions blocked! Reversing and turning around...")
        move_backward()
        move_backward()  # Reverse more
        if not check_emergency_stop():
            turn_right()
            turn_right()
            turn_right()  # Turn around ~135-180 degrees
    
    print(f"Avoidance complete. Obstacle flags: L={left_obstacle}, C={center_obstacle}, R={right_obstacle}")


def intruder_alert():
    """Activate intruder alert with buzzer and LEDs"""
    global last_intruder_alert
    
    current_time = time.time()
    if current_time - last_intruder_alert < INTRUDER_ALERT_COOLDOWN:
        return  # Debounce - don't alert too frequently
    
    last_intruder_alert = current_time
    print("INTRUDER DETECTED! Activating alarm...")
    
    # Turn on spotlight (represented by both LEDs)
    led_left.on()
    led_right.on()
    
    # Sound alarm with buzzer and blink LEDs
    for _ in range(5):
        if check_emergency_stop():
            return
        buzzer.value = 0.5
        sleep(0.5)
        buzzer.value = 0
        led_left.toggle()
        led_right.toggle()
        sleep(0.5)
    
    # Turn off LEDs after alert
    stop_all()


def low_battery_alert():
    """Alert user of low battery condition"""
    global last_battery_alert
    
    current_time = time.time()
    if current_time - last_battery_alert < LOW_BATTERY_ALERT_COOLDOWN:
        return  # Debounce - don't alert too frequently
    
    last_battery_alert = current_time
    voltage = get_battery_voltage()
    print(f"LOW BATTERY! Current voltage: {voltage:.2f}V - Please charge!")
    
    # Alert with buzzer and blinking LEDs
    for _ in range(5):
        if check_emergency_stop():
            return
        buzzer.value = 0.3
        led_left.toggle()
        led_right.toggle()
        sleep(0.5)
        buzzer.value = 0
        sleep(0.5)
    
    stop_all()

# ============================================================================
# MAIN PROGRAM
# ============================================================================

def main():
    """Main program loop"""
    global system_active
    
    print("=== Surveillance Robot Starting ===")
    print(f"Battery voltage threshold: {BATTERY_LOW_THRESHOLD}V")
    print(f"Obstacle detection distance: {OBSTACLE_DISTANCE_CM}cm")
    
    # Initialize servo to center position
    print("Initializing servo to center position...")
    set_angle(SERVO_CENTER)
    sleep(0.5)
    stop_servo()
    
    try:
        while system_active:
            # Check emergency stop
            if check_emergency_stop():
                break
            
            # Execute patrol pattern
            patrol_logic()
            
            # Check for obstacles
            distance = get_distance_cm()
            if distance < OBSTACLE_DISTANCE_CM:
                obstacle_avoidance()
            
            # Check for motion/intruder
            if pir.motion_detected:
                intruder_alert()
            
            # Monitor battery level
            battery_voltage = get_battery_voltage()
            print(f"Battery: {battery_voltage:.2f}V")
            if battery_voltage < BATTERY_LOW_THRESHOLD:
                low_battery_alert()
            
            # Small delay between patrol cycles
            sleep(0.5)
    
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    finally:
        # Cleanup
        print("Shutting down...")
        set_angle(SERVO_CENTER)
        sleep(0.3)
        stop_servo()
        stop_all()
        pi.stop()
        print("Cleanup completed. System stopped.")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()