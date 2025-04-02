#!/usr/bin/env python3
from time import *
start_timer = time()
struct = localtime(start_timer)
print("Start Countdown at :",strftime("%X",struct))

i =10
while i>0:
    print(i)
    i-=1
    sleep(1)

end_timer  =time()
print("Stop Countdown at :",strftime("%X",struct))
difference = round(end_timer - start_timer)

print("\nRunTime", difference,"Seconds")

#day = today.strftime("%A")
#month = today.strftime("%B")
#tax = item*rate
#total  = item + tax

#print("Date", day, month, today.day)
#print("Tax:\t", "{:.2f} ".format( tax))
#print("Total:\t", "{:.2f} ".format(total))

#num =4
#print(num , "Squared:", math.pow(num,2))
#print(num , "Square root:", math.sqrt(num))

#nums = random.sample (range(1,48),7)
#print("Your lucky Lotto number is ", nums)

