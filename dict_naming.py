#!/usr/bin/env python3

info = {"Name":"Andrew","ref":"Python","Sys":"Win"}
print("Info", type(info))
print("Dictionary",info)

print("\n Reference",info["ref"])
print("\n keys", info.keys())
#students = {"Andrew","Kelly","Lynn","David"}
#commons = party_goers.intersection(students)

del info["Name"]
info["user"] = "Tom" 
print("\n Dictionary",info)
print("\nIs there a name key", "name" in info)

#print("First student at the party",party_students[0])



