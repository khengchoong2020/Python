#!/usr/bin/env python3
def copy_sort( array ):
    copy = array[:]
    sorted_copy = []

    while len( copy )>0:
        minimum = 0
        #element = 0
        for element in range(len(copy)):
            if copy[ element ] < copy[ minimum ]:
                minimum  = element
        print ("\tRemoving", copy[ minimum ] , "from", copy)

        sorted_copy.append(copy.pop( minimum ))
        print("\n \t", copy)

    return sorted_copy

array =[5,3,1,2,6,4]
print("Copy Sort...\nArray",array)
print("Copy:",copy_sort( array ))
print("Array:",array)


#print("Hello")
