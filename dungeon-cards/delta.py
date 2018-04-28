#!/usr/bin/python3
#
# vector that gets you from l1 to l2

class delta():
    def init(self, l1, l2):
        self.dr = l2.r - l1.r
        self.dc = l2.c - l1.c

    def add(self, loc):
        return (loc.r + self.dr, loc.c + self.dc)

