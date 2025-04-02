#!/usr/bin/env python3
from decimal import *
rate = Decimal(1.05)
item = Decimal(0.70)

tax = item*rate
total  = item + tax

print("Item:\t", "{:.2f} ".format(item))
print("Tax:\t", "{:.2f} ".format( tax))
print("Total:\t", "{:.2f} ".format(total))

#num =4
#print(num , "Squared:", math.pow(num,2))
#print(num , "Square root:", math.sqrt(num))

#nums = random.sample (range(1,48),7)
#print("Your lucky Lotto number is ", nums)

