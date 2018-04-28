#!/usr/bin/python3

class loc():
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __str__(self):
        return "(%d, %d)" % (self.r, self.c)
    
