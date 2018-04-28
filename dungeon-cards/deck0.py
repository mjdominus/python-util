#!/usr/bin/python3

from card import card

# Simplest possible deck
# Contains:
#   Coins (worth 1) 
#   Traps (deadly)
#
# with equal probability

class deck():
    def __init__(self, game):
        self.g = game

    # generate a random card
    def deal(self):
        r = self.g.random.true_random(2)
        if r == 0:
            return card(self.g, "coin", 1, None)
        else:
            return card(self.g, "trap", 1, None)
    
