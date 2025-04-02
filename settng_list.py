#!/usr/bin/env python3

party_goers = {"Andrew","Barbara","Carole","David"}
print("party_goers", type(party_goers))
print("Did david go to the party","David" in party_goers)
print("Did Kelly go to the party","Kelly" in party_goers)
#print("Hello")
students = {"Andrew","Kelly","Lynn","David"}
commons = party_goers.intersection(students)

party_students = list(commons)
print("Students at the party",party_students)
print("First student at the party",party_students[0])



