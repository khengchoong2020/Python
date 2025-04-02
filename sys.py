#!/usr/bin/env python3
import sys, keyword
print("Python version", sys.version)
print("Python interpreter location", sys.executable)
print("Python module search path")
for folder in sys.path:
    print(folder)




