from gpiozero import DistanceSensor
import pigpio
import time

SERVO_PIN = 18
pi = pigpio.pi()
if not pi.connected:
  exit()

def set_angle(angle):
  
