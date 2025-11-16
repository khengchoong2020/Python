'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = SHARP IR sensor GP2Y0A21 control via ADC MCP3008 on Raspberry Pi 3B
            = IR sensor measures distance using infrared reflection
            = MCP3008 channel 0 for IR sensor analog-to-digital conversion
            = Value range: 0.0 to 1.0 (representing 0V to 3.3V)
'''

from gpiozero import MCP3008
from time import sleep

# Initialize IR sensor on MCP3008 channel 0
ir_sensor = MCP3008(0)

# Configuration
REFERENCE_VOLTAGE = 3.3  # MCP3008 reference voltage (3.3V for Raspberry Pi)
IR_SENSOR_MIN_VOLTAGE = 0.42  # Minimum voltage for GP2Y0A21 (no object detected)


def get_voltage():
    """
    Get raw voltage reading from IR sensor.
    
    Returns:
        float: Voltage in volts (0.0 to 3.3V)
    """
    return ir_sensor.value * REFERENCE_VOLTAGE


def calculate_distance(voltage):
    """
    Convert IR sensor voltage to distance using GP2Y0A21 formula.
    
    Args:
        voltage: Voltage reading from sensor
    
    Returns:
        float: Distance in centimeters (or -1 if calculation fails)
    """
    try:
        if voltage <= IR_SENSOR_MIN_VOLTAGE:
            return float('inf')  # Object too far or out of range
        
        # GP2Y0A21 formula: distance = 27.86 / (voltage - 0.42)
        distance = 27.86 / (voltage - IR_SENSOR_MIN_VOLTAGE)
        return distance
    except Exception as e:
        print(f"Error calculating distance: {e}")
        return -1


def main():
    """Main loop to read IR sensor and display distance."""
    try:
        print("\n" + "=" * 60)
        print("SHARP IR Sensor (GP2Y0A21) - Distance Measurement")
        print("=" * 60)
        print(f"MCP3008 Channel: 0")
        print(f"Reference Voltage: {REFERENCE_VOLTAGE}V")
        print(f"Value Range: 0.0 to 1.0")
        print(f"Voltage Range: 0V to {REFERENCE_VOLTAGE}V")
        print("Press Ctrl+C to stop\n")
        
        while True:
            # Get raw value and voltage
            raw_value = ir_sensor.value
            voltage = get_voltage()
            
            # Calculate distance
            distance = calculate_distance(voltage)
            
            # Display results
            print(f"Raw Value: {raw_value:.4f} | Voltage: {voltage:.2f}V | Distance: {distance:.2f} cm")
            
            sleep(1)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("Program stopped by user")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
