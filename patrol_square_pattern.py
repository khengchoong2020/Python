'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-15
Description = Square pattern patrol for Raspberry Pi 3B robot
            = Robot moves in a square: Forward → Right Turn → Forward → Right Turn (repeat)
            = LEDs indicate movement direction:
            = - Forward: Both LEDs ON steady
            = - Right Turn: Right LED blinks at 10ms
            = - Left Turn: Left LED blinks at 10ms
            = - Stop: Both LEDs OFF
'''

from gpiozero import LED
from time import sleep

# GPIO pin assignments
LED_LEFT = LED(17)
LED_RIGHT = LED(23)

# Configuration
FORWARD_DURATION = 2      # Seconds to move forward
TURN_DURATION = 2         # Seconds to turn
SQUARE_SIDES = 4          # Number of sides in square (always 4)
BLINK_INTERVAL = 0.01     # LED blink interval in seconds (10ms)

# State tracking
patrol_active = False
square_count = 0


def move_forward(duration=FORWARD_DURATION):
    """
    Move robot forward.
    LEDs: Both ON (steady light)
    
    Args:
        duration: Time in seconds to move forward
    """
    print("[FORWARD] Moving forward...")
    LED_LEFT.on()
    LED_RIGHT.on()
    sleep(duration)
    LED_LEFT.off()
    LED_RIGHT.off()


def turn_right(duration=TURN_DURATION):
    """
    Turn robot right.
    LEDs: Right LED blinks at 10ms interval
    
    Args:
        duration: Time in seconds to turn
    """
    print("[RIGHT TURN] Turning right...")
    LED_LEFT.off()
    
    # Blink right LED rapidly
    blink_count = int(duration / (BLINK_INTERVAL * 2))  # Account for on/off cycle
    for _ in range(blink_count):
        LED_RIGHT.toggle()
        sleep(BLINK_INTERVAL)
    
    LED_RIGHT.off()


def turn_left(duration=TURN_DURATION):
    """
    Turn robot left.
    LEDs: Left LED blinks at 10ms interval
    
    Args:
        duration: Time in seconds to turn
    """
    print("[LEFT TURN] Turning left...")
    LED_RIGHT.off()
    
    # Blink left LED rapidly
    blink_count = int(duration / (BLINK_INTERVAL * 2))  # Account for on/off cycle
    for _ in range(blink_count):
        LED_LEFT.toggle()
        sleep(BLINK_INTERVAL)
    
    LED_LEFT.off()


def stop_movement():
    """
    Stop robot movement.
    LEDs: Both OFF
    """
    print("[STOP] Stopping robot...")
    LED_LEFT.off()
    LED_RIGHT.off()


def square_patrol_cycle():
    """
    Execute one complete square pattern cycle.
    
    Sequence:
    1. Move Forward
    2. Turn Right 90°
    3. Move Forward
    4. Turn Right 90°
    5. Move Forward
    6. Turn Right 90°
    7. Move Forward
    8. Turn Right 90° (back to starting position)
    """
    global square_count
    
    square_count += 1
    print("\n" + "=" * 60)
    print(f"SQUARE PATROL CYCLE #{square_count}")
    print("=" * 60 + "\n")
    
    for side in range(SQUARE_SIDES):
        # Move forward on each side
        print(f"Side {side + 1}/{SQUARE_SIDES}:")
        move_forward(FORWARD_DURATION)
        
        # Turn right at corner (except after last side)
        if side < SQUARE_SIDES - 1 or square_count > 1:
            turn_right(TURN_DURATION)
        
        sleep(0.5)  # Brief pause between moves
    
    print("\n✓ Square patrol cycle complete!\n")


def main():
    """Main program loop for square pattern patrol."""
    global patrol_active
    
    try:
        print("\n" + "=" * 60)
        print("SQUARE PATTERN PATROL - Raspberry Pi 3B")
        print("=" * 60)
        print("Robot moves in a square pattern with LED indicators")
        print("Forward: Both LEDs ON")
        print("Turn Right: Right LED blinks")
        print("Turn Left: Left LED blinks")
        print("Stop: Both LEDs OFF")
        print("Press Ctrl+C to stop\n")
        
        patrol_active = True
        
        while patrol_active:
            square_patrol_cycle()
            
            # Optional: Wait between cycles
            sleep(1)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Program stopped by user")
        print(f"Total completed squares: {square_count}")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")
        
    finally:
        # Cleanup
        stop_movement()
        LED_LEFT.off()
        LED_RIGHT.off()
        print("Cleanup completed")


if __name__ == '__main__':
    main()
