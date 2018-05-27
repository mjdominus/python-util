#!/usr/bin/python3

from card import card
from cardtype import cardtype
import action

# Simplest possible deck
# Contains:
#   Coins (worth 1) 
#   Traps (deadly)
#
# with equal probability


cardtype("coin", { "attacked": [action.simple_coin()] })
cardtype("trap", { "attacked": [action.simple_trap()] })


class deck():
    def __init__(self, game):
        self.g = game

    # generate a random card
    def deal(self):
        r = self.g.random.true_random(2)
        if r == 0:
            return card(self.g, "coin", 1)
        else:
            return card(self.g, "trap", 1)
    
