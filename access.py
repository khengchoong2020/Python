#!/usr/bin/env python3
file =open("example.txt", "w+")

print("File name",file.name)
print("\nFile open mode",file.mode)

print("\nReadable:",file.readable())
print("\nWriteable:",file.writable())

def get_status(f):
    if not f.closed:
        return "Open"
    else:
        return "Close"
print("\nFile status:",get_status(file))
file.close()
print("\nFile status:",get_status(file))


