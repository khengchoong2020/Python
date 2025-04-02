#!/usr/bin/env python3
from Dog import *


henry = Dog("Knight Forest", "Golden Retriever", 1)
my_dog = Dog("Mountain", "German Shepherd", 2)

# Accessing attributes and calling methods
print(my_dog.name)  # Output: Buddy
print(henry.description())  # Output: Max is a 5-year-old German Shepherd.
print("count = ",henry.count)
my_dog.bark()  # Output: Buddy says Woof!print("\nClass instructor of \n", Bird.__doc__)
Hin_Soon = Dog("Ichikawa","Chiwawa", 3)
print("Hin Soon'age", Hin_Soon.age)
Hin_Soon.age =  54
print("Hin Soon'age", Hin_Soon.age)

setattr(Hin_Soon,"age", 64)
print("Hin Soon'age", Hin_Soon.age)

print("\nHin Soon attributes...")
for attrib in dir(Hin_Soon):
    if attrib[0]!="_":
        print(attrib,":", getattr(Hin_Soon,attrib))
delattr(Hin_Soon,"age")
print("\nHin Soon age attribute", hasattr(Hin_Soon, "age"))
#print(my_dog.bark)

