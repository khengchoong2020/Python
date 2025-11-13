import pigpio
import time

SERVO_PIN = 18

pi = pigpio.pi()
if not pi.coonected:
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
  pulse width = int (500+(angle* 2000/180))
  pi.set_servo_pulsewidth(SERVO_PIN, pulse_width)

def stop_servo()
  pi.set_servo_pulse_width(SERV)_PIN,0)

try:
  for angle in range(0, 181, 30):
    set_angle(angle)
    sleep(0.5)

finally:
  stop_servo()
  pi.stop()

