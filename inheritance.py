#!/usr/bin/env python3
from Rectangle import *
from Triangle import *

rect = Rectangle()
tria = Triangle()

rect.Set_Values(4,5)
tria.Set_Values(4,5)

print("Rectangle Area", rect.area())
print("Triangle Area", tria.area())
