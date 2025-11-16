from gpiozero import LED
from time import sleep

# pin setup
LED_left = LED(17)
LED_right = LED(27)

def LED_BLINK(count, interval, left = True, right = True):
  """BLINK LEDs based on flags using toggle."""
  for _ in range(count):
    if left :
      LED_left.toggle()
    if right :
      LED_right.toggle()
    sleep(interval)
  
  

def forward():
  LED_left.on()
  LED_right.on()

def backward():
  # Both LEDs blink at 100ms for 2 seconds
  LED_BLINK(count =20, interval = 0.1, left = True, right = True)
  sleep(1)
  LED_left.off()
  LED_right.off()  

def right_turn():
  LED_BLINK(count =20, interval = 0.1, left = False, right = True)
  sleep(1)
  LED_left.off()
  LED_right.off()  
  

def left_turn():
  LED_BLINK(count =20, interval = 0.1, left = True, right = False)
  sleep(1)
  LED_left.off()
  LED_right.off()  

def stop():
  LED_left.off()
  LED_right.off()  

def main():
  try:
    while True:
      forward()
      sleep(2)
      stop()
      sleep(1)
      backward()
      sleep(1)
      left_turn()
      sleep(1)
      right_turn()
      sleep(1)
  except KeyboardInterrupt:
    print("Program stopped by User")
  finally:
    LED_left.off()
    LED_right.off()

if __name__ == "__main__":
  main()