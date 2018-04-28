#!/usr/bin/python3

from move import move
from loc import loc

class player():
    def __init__(self, game):
        self.g = game

    def initialize(self):
        pass

    def move(self):
        print("You are at " + str(self.g.board.find_player()))
        print("Move to? ")
        return move("move", loc(1, 2))

    
