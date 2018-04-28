#!/usr/bin/python3

def location():
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def neighbors(self):
        n = []
        for i in range(3):
            _i = abs(i - self.r)
            for j in range(3):
                _j = abs(j - self.c)
                if _i + _j == 1:
                    n.append(location(i, j))
        return n

