#!/usr/bin/env python3

import sys

print(sys.version)

import os

print(sys.executable)

folder = os.listdir('.')  # Assuming you want to list the current directory
for item in folder:
    print(item)
