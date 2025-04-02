#!/usr/bin/env python3
class Bird:
    ''' A class to define bird properties  '''
    count = 0

    def __int__(self, chat):
        self.sound = chat
        Bird.count +=1

    def talk(self):
        return f"{self.sound}"
