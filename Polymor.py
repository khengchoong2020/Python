#!/usr/bin/env python3
from Duck import *
from Mouse import *

def Describe(object):
    object.Talk()
    object.Coat()

dolly = Duck()
monty = Mouse()

Describe(dolly)
Describe(monty)
