#!/usr/bin/env python3
num1 = input("Please enter a whole number.")
num2 = input("Please enter another whole number.")

print(num1 ,"is", type(num1))
print(num2 ,"is", type(num2))

total = num1 + num2
print("Total" ,total, type(total) )

total = int(num1) + int(num2)
print("Total" ,total, type(total) )

total = float(num1) + float(num2)
print("Total" ,total, type(total) )
