from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
import pigpio
from time import sleep

SERVO_PIN = 18
sensor = DistanceSensor(echo=15, trigger=14, max_distance = 4, pin_factory = PiGPIOFactory())

pi = pigpio.pi()
if not pi.connected:
  exit()

def set_angle(angle):
  """
  convert angle to pulse width and set servo position
  angle : 0 -180 degrees
  pulse width: 500 ~2500 microsecs
  """
  if not 0 <= angle <= 180:
    raise ValueError("Angle must be between 0 and 180 degrees")

  # convert angle to pulse width (microseconds)
  # 500us (0 deg) to 2500us (180 deg)
  pulse_width = int (500+(angle* 2000/180))
  pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

def stop_servo():
  pi.set_servo_pulse_width(SERVO_PIN,0)

def get_distance():
    try:
        return sensor.distance * 100  # convert to cm and sensor is ultrasonic
    except Exception as e:
        print(f"Error reading distance: {e}")



def main():
  try:
    while True:
      for angle in range(0, 181, 30):
        set_angle(angle)
        sleep(0.5)

  except KeyboardInterrupt:
    print("Program stopped by User")

  finally:
    stop_servo()
    pi.stop()
  
if __name__ == '__main__':
  main()


