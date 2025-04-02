#!/usr/bin/env  python3
from Bird import *

print("\nClass instructor of \n", Bird.__doc__)

polly = Bird("Woof")  # Corrected bird instantiation.
print("\nNumber of Birds", Bird.count)
print(polly.talk())
