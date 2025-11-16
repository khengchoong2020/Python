'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-15
Description = Obstacle detection using SG90 microservo and ultrasonic sensor
            = Scans three directions: LEFT (45°), CENTER (90°), RIGHT (135°)
            = Reports obstacles using boolean values (True = obstacle detected, False = clear)
            = Obstacle threshold: distance < 20cm
'''

from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import pigpio
from time import sleep

# Configuration
SERVO_PIN = 18
OBSTACLE_THRESHOLD_CM = 20

# Scan angles
ANGLE_LEFT = 0      # Left direction
ANGLE_CENTER = 90    # Center direction
ANGLE_RIGHT = 180    # Right direction

# Initialize ultrasonic sensor
sensor = DistanceSensor(echo=15, trigger=14, max_distance=4, pin_factory=PiGPIOFactory())

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")


def set_angle(angle):
    """
    Convert angle to pulse width and set servo position.
    
    Args:
        angle: 0-180 degrees
    
    Pulse width: 500-2500 microseconds
    """
    if not 0 <= angle <= 180:
        raise ValueError("Angle must be between 0 and 180 degrees")
    
    # Convert angle to pulse width (microseconds)
    # 500µs (0°) to 2500µs (180°)
    pulse_width = int(500 + (angle * 2000 / 180))
    pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)


def stop_servo():
    """Stop sending pulses to servo to save power."""
    pi.set_servo_pulsewidth(SERVO_PIN, 0)


def get_distance_cm():
    """
    Get distance from ultrasonic sensor in centimeters.
    
    Returns:
        float: Distance in cm, or 999 if error occurs
    """
    try:
        return sensor.distance * 100  # Convert to cm
    except Exception as e:
        print(f"Error reading distance: {e}")
        return 999  # Return large value on error


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


def main():
    """Main program loop for obstacle detection."""
    try:
        print("\n" + "=" * 60)
        print("Obstacle Detection System - SG90 Servo + Ultrasonic Sensor")
        print("=" * 60)
        print(f"Obstacle Threshold: {OBSTACLE_THRESHOLD_CM} cm")
        print("Press Ctrl+C to stop\n")
        
        while True:
            # Scan obstacles in all three directions
            results = scan_obstacles()
            
            # Report findings
            report_obstacles(results)
            
            # Wait before next scan
            sleep(2)
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        print("Returning servo to center position...")
        set_angle(ANGLE_CENTER)
        sleep(0.3)
        stop_servo()
        pi.stop()
        print("Cleanup completed")


if __name__ == '__main__':
    main()
