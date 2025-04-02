#!/usr/bin/env python3

def echo(user, lang, sys):
    print("User",user, "lang" , lang, "sys", sys)

echo("mike", "Python", "Windows")
echo(user="John", lang="Python", sys="Windows")

def miror(user ="Carole", lang = "Python" ):
    print("\nUser",user, "Language",lang)

miror()
miror(lang = "Java")
miror("Tony")
miror("Susan","C++")


