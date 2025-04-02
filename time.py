#!/usr/bin/env python3
from datetime import datetime
today = datetime.today()
print("Today is:",today)

for attr in ["year","month","day","hour", "minute","second", "microsecond"]:
    print(attr,"\t", getattr(today, attr))

print("Time", today.hour,":", today.minute, sep = "")

day = today.strftime("%A")
month = today.strftime("%B")
#tax = item*rate
#total  = item + tax

print("Date", day, month, today.day)
#print("Tax:\t", "{:.2f} ".format( tax))
#print("Total:\t", "{:.2f} ".format(total))

#num =4
#print(num , "Squared:", math.pow(num,2))
#print(num , "Square root:", math.sqrt(num))

#nums = random.sample (range(1,48),7)
#print("Your lucky Lotto number is ", nums)

