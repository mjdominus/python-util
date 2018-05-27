#!/usr/bin/python3
#
# vector that gets you from l1 to l2

from loc import loc

class delta():
    def __init__(self, l1, l2):
        self.dr = l2.r - l1.r
        self.dc = l2.c - l1.c

    def add(self, p):
        return loc(p.r + self.dr, p.c + self.dc)

