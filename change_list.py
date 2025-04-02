#!/usr/bin/env python3
basket=["Apple","Bun", "Cola"]
crate= ["Egg","Fig", "Grape"]

print("Basket list", basket)
print("Basket element", len(basket))

basket.append("Damson")
#print("Third month", quarter[2])
print("Appended", basket)
print("last item removed", basket.pop())
print("basket list", basket)

basket.extend(crate)
print("Extended", basket)
del basket[1]
print("item removed", basket)
del basket[1:3]
print("slice removed", basket)



