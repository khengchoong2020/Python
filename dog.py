#!/usr/bin/env python3
class Dog:
    """A simple class representing a dog."""
    count =0

    def __init__(self, name, breed, age):
        """Initialize name, breed, and age attributes."""
        self.name = name
        self.breed = breed
        self.age = age
        Dog.count +=1

    def bark(self):
        """Simulate a dog barking."""
        print(f"{self.name} says Woof!")

    def description(self):
        """Return a formatted string describing the dog."""
        return f"{self.name} is a {self.age}-year-old {self.breed}."
