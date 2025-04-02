#!/usr/bin/env python3
class Person:
    """A simple class representing person."""

    def __init__(self, name ):
        self.name = name

    def Speak(self, msg = "(calling the Base class)"):
        print(self.name, msg)
