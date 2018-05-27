#!/usr/bin/python3

from move import move
from loc import loc

class player():
    def __init__(self, game):
        self.g = game
        self.canned_moves = [ move("move", loc(1,2)) ]

    def initialize(self):
        pass

    def move(self):
        print("You are at " + str(self.g.board.find_player()))
        print("Move to? ")
        if self.canned_moves:
            m = self.canned_moves.pop(0)
        else:
            m = move("quit")
        print("Move: %s" % str(m))
        return m

    
