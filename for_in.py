#!/usr/bin/env python3

chars=["A","B","C"]
fruit =("Apple", "Banana", "Cherry")
info={"Name":"John", "ref":"Python","sys":"win"}

print("Elements: \t", end = " ")
for item in chars:
    print(item, end = " ")

print("\nEnumerated:\t", end = " ")
for item in enumerate(chars):
    print(item, end = " ")

print("\nZipped:\t", end = " ")
for item in zip(chars,fruit):
    print(item, end = " ")

print("\nPaired:\t", end = " ")
for key,value in info.items():
    print(key, " = ", value)

