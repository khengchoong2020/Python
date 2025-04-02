#!/usr/bin/env python3
import sys, keyword
#print("keyword false",iskeyword("false"))
print("Python Module search path")
for folder in sys.path:
    print(folder)
print("Python Keyword")
for word in keyword.kwlist:
    print(word)

