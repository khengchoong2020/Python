#!/usr/bin/env python3

global_var =1

def my_var():
    """ This function demonstrates the use of global and local variables."""
    print("Global Variable", global_var)

    local_var =2
    print("Local variable", local_var)

    global inner_var
    inner_var=3


my_var()
print("Second variable", inner_var)
print(input.__doc__)