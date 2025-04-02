#!/usr/bin/env python3
from Man import *
from Hombre import *

guy1 = Man("Richard")
guy2 = Hombre("Ricardo")

guy1.Speak("It's a beutiful evening\n")
guy2.Speak("Es una tarde hermosa\n")

Person.Speak(guy1)
Person.Speak(guy2)
