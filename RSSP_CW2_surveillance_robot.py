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
            - intruder alertusing PIR = Buzzer sound
            - low battery level alerrt = blinking and buzzer soung
            :task 4 (power management)
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
import pigpio
from time import sleep
import time

battery_voltage_divider = 3.0
battery_low_threshold = 6.5  # example threshold for low battery
battery_reference_voltage = 3.3

obstacle_distance_threshold = 20  # in cm

intruder_alert_colddown = 30
low_battery_alert_cooldown = 60

servo_center_angle = 90
servo_scan_angles = range(0, 181, 30)

emergency_stop_pin = 27  # GPIO pin for emergency stop switch



# GPIO Initialization 
pi = pigpio.pi()
if not pi.connected:
    exit("Failed to connect to pigpio daemon. Run 'sudo pigpiod' first.")
# GPIO pin for servo
SERVO_PIN = 18
LEDLeft = LED(17)
LEDRight = LED(23)
pir = MotionSensor(4)    # GPIO4
ir_sensor = MCP3008(0)  # assuming the sensor is connected to channel 0
battery_level_sensor = MCP3008(1)  # channel 1 for battery level detection
voltage_monitor_sensor = MCP3008(2)  # channel 2 for voltage monitoring
buzzer = PWMOutputDevice(22, frequency = 440, initial_value =0)
ultrasonic_echo = 15
ultrasonic_trigger = 14
sensor = DistanceSensor(echo=ultrasonic_echo, trigger=ultrasonic_trigger)

emergency_stop = Button(emergency_stop_pin, pull_up=True, bounce_time=0.1)
system_active = True

last_intruder_alert = 0
last_battery_alert = 0
servo_angle = servo_center_angle

left_obbstacle = 0
right_obstacle = 0
center_obstacle = 0

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

def stop_servo()
    pi.set_servo_pulsewidth(SERVO_PIN, 0)

def get_distance():
    try:
        return sensor.distance * 100  # convert to cm and sensor is ultrasonic
    except Exception as e:
        print(f"Error reading distance: {e}")

def get_battery_voltage():
    adc_value = battery_level_sensor.value  # MCP3008 value between 0 and 1
    voltage = adc_value * battery_reference_voltage * battery_voltage_divider
    return voltage

def check_emergency_stop():    
    global system_active
    if not emergency_stop.is_pressed:
        system_active = False
        print("Emergency stop activated! Shutting down the system.")
        stop_all()
    return False

def stop_all():
    LEDLeft.off()
    LEDRight.off()
    stop_servo()
    buzzer.value = 0
    pi.stop()

def blink_leds(times, interval, left_led=True, right_led=True):
    for _ in range(times):
        if check_emergency_stop():
            return
        if left_led:
            LEDLeft.toggle()            
        if right_led:
            LEDRight.toggle()
        sleep(interval)
    
    if left_led:
        LEDLeft.off()
    if right_led:
        LEDRight.off()

def patrol_logic():
    # Forward movement
    LEDLeft.on()
    LEDRight.on()
    sleep(1)

    # Backward movement
    for _ in range(5):
        LEDLeft.toggle()
        LEDRight.toggle()
        sleep(0.1)

    # Right turn
    for _ in range(5):
        LEDRight.toggle()
        sleep(0.01)

    # Left turn
    for _ in range(5):
        LEDLeft.toggle()
        sleep(0.01)
    # Stop
    LEDLeft.off()
    LEDRight.off()
    sleep(1)

def obstacle_avoidance():
    print("Obstacle detected! Initiating avoidance maneuvers.")
    # Stop movement
    LEDLeft.off()
    LEDRight.off()
    sleep(1)

    # Scan surroundings
    for angle in range(0, 181, 30):
        set_angle(angle)
        sleep(0.5)
        distance = sensor.distance * 100  # convert to cm
        print(f"Angle: {angle}, Distance: {distance:.2f} cm")
        if distance > 20:
            print("Clear path found!")
            break

    # Reverse and turn slightly
    for _ in range(5):
        LEDLeft.toggle()
        LEDRight.toggle()
        sleep(0.1)
    LEDLeft.on()
    sleep(1)

def intruder_alert():
    print("Intruder detected! Activating alarm.")
    for _ in range(5):
        buzzer.value = 0.5
        LEDLeft.toggle()
        LEDRight.toggle()
        sleep(0.5)
        buzzer.value = 0
        sleep(0.5)

def low_battery_alert():
    print("Low battery level! Activating alert.")
    for _ in range(5):
        buzzer.value = 0.5
        LEDLeft.toggle()
        LEDRight.toggle()
        sleep(0.5)
        buzzer.value = 0
        sleep(0.5)

def main():
    try:
        while True:
            patrol_logic()

            # Obstacle detection
            distance = sensor.distance * 100  # convert to cm
            if distance < 20:
                obstacle_avoidance()

            # Motion detection
            if pir.motion_detected:
                intruder_alert()

            # Battery level monitoring
            battery_level = battery_level_sensor.value * 3.3  # assuming 3.3V reference
            if battery_level < 3.5:  # example threshold for low battery
                low_battery_alert()

            sleep(1)

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