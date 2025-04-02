#!/usr/bin/env python3
import random

num = random.randint(1,20)
flag = True
guess =""

print("Guess my number 1-20:", end =" ")

while flag:
    guess = input()
    if not guess.isdigit():
        print("Invalid Number")
        break
    elif int(guess) < num:
        print("Too low, try again: ", end="")
    elif int(guess) > num:
        print("Too high, try again: ", end="")
    else:
        print("correct!")
        flag =False





