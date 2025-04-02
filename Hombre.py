#!/usr/bin/env python3
from Person import *
class Hombre(Person):
    """A simple class representing polygon."""

    def Speak(self,msg):
        print(self.name,"\n\tHola", msg)
