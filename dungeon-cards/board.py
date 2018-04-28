#!/usr/bin/python3
#
# Handles all queries about what is where
# and _especially_ all requests to move things

class board():
    def __init__(self):
        self.b = [ [None, None, None],
                   [None, None, None],
                   [None, None, None],
                 ]
        for r in range(3):
            for c in range(3):
                self.b[r][c] = GAME.random.random_card("Random card for (%d,%d)" % (r, c))

    def find(self, what):
        for r in range(3):
            for c in range(3):
                if self.b[r][c].kind_is(what):
                    return (r,c)
        return None

    def swap(self, loc_1, loc_2):
        m1 = self.get(loc_1)
        m2 = self.get(loc_2)
        self.set(loc_1, m2)
        self.set(loc_2, m1)

    def get(self, loc):
        return self.b[loc.r][loc.c]

    def set(self, loc, m):
        self.b[loc.r][loc.c] = m
        m.moved(loc)
        
    
