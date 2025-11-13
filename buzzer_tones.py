'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = Control buzzer frequency using gpiozero TonalBuzzer
'''

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
from time import sleep

# Create a TonalBuzzer on GPIO pin (change to your pin number)
buzzer = TonalBuzzer(17)  # Use your GPIO pin number here

def play_frequency(freq, duration):
    """Play a specific frequency for given duration"""
    buzzer.play(Tone.from_frequency(freq))
    sleep(duration)
    buzzer.stop()
    sleep(0.1)  # Brief pause between tones

def main():
    try:
        # Example 1: Play different frequencies
        frequencies = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5 scale
        for freq in frequencies:
            print(f"Playing {freq}Hz")
            play_frequency(freq, 0.5)
        
        # Example 2: Siren effect (sliding frequency)
        print("Playing siren effect")
        for _ in range(3):
            for freq in range(500, 2000, 100):
                buzzer.play(Tone.from_frequency(freq))
                sleep(0.05)
            for freq in range(2000, 500, -100):
                buzzer.play(Tone.from_frequency(freq))
                sleep(0.05)
        
        # Example 3: Play some common musical notes
        notes = {
            'C4': 262,
            'D4': 294,
            'E4': 330,
            'F4': 349,
            'G4': 392,
            'A4': 440,
            'B4': 494,
            'C5': 523
        }
        
        print("Playing musical notes")
        for note, freq in notes.items():
            print(f"Playing {note} ({freq}Hz)")
            play_frequency(freq, 0.3)

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    finally:
        buzzer.stop()
        print("Buzzer stopped")

if __name__ == '__main__':
    main()