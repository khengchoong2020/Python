'''
Author      = KOH KHENG CHOONG
Date        = 2025-11-02
Description = this is a python code with raspberry pi 3B to Control buzzer functionality
            = 

'''

from gpiozero import PWMOutputDevice
from time import sleep
buzzer = PWMOutputDevice(22, frequency = 440, initial_value =0)

#buzzer.play(Tone.from_frequency(440))  # Play 440 Hz (A4 note)
#sleep(1)
#buzzer.stop()
'''
C4: 262 Hz
D4: 294 Hz
E4: 330 Hz
F4: 349 Hz
G4: 392 Hz
A4: 440 Hz
B4: 494 Hz
C5: 523 Hz
'''

def main():
#    buzzer = Buzzer(22)
    try:
        while True:
            buzzer.value = 1.0
            print("Buzzer ON")
            sleep(0.05)
            buzzer.value = 0
            print("Buzzer OFF")
            sleep(0.05)
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        buzzer.off()
        print("Buzzer turned off")

if __name__ == '__main__':
	main()
