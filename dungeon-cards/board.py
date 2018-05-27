#!/usr/bin/python3
#
# Handles all queries about what is where
# and _especially_ all requests to move things

from loc import loc
from delta import delta

class board():
    def __init__(self, game):
        self.b = [ [None, None, None],
                   [None, None, None],
                   [None, None, None],
                 ]
        self.g = game

    def initialize(self, player):
        for r in range(3):
            for c in range(3):
                if r == 1 and c == 1:
                    self.set(loc(r, c), player)
                else:
                    self.fill(loc(r, c))

    def fill(self, loc):
        self.set(loc, self.g.deck.deal())

    def find(self, what):
        for r in range(3):
            for c in range(3):
                a_loc = loc(r, c)
                if self.get(a_loc).kind_is(what):
                    return a_loc
        return None

    def find_player(self):
        return self.find("player")

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

    # move player to new position, eliminating
    # the card that was there before
    # this determines how the cards slide around when
    # the player moves
    def snuff_me(self, card):
        d = delta(self.g.player_card.loc, card.loc)
        cur_loc = card.loc
        while True:
            next_loc = d.add(cur_loc)
            if not self.is_valid_loc(next_loc): break
            self.set(next_loc, self.get(cur_loc))
            cur_loc = next_loc
        # At this point cur_loc needs to be filled with a new card
        self.fill(cur_loc)
        

    def is_valid_loc(self, loc):
        return loc.r >= 0 and loc.r < 3 \
           and loc.c >= 0 and loc.c < 3