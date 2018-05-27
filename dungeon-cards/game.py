#!/usr/bin/python3

from board import board
from deck0 import deck
from interactive_player import player
from card import card
from cardtype import card_library
from cardtype import cardtype
from interactive_random import random

class game():
    def __init__(self):
        self.board = board(self)
        self.deck = deck(self)
        self.random = random()
        self.player = player(self)
        self.player_card = card(self, "player", 10)
        self.score = 0
        self.turns = 0
        self.game_over = False
        self.player = player(self)

    def initialize(self):
        self.board.initialize(player=self.player_card)
        self.player.initialize()

    def play(self):
        self.initialize()
        while not self.game_over:
            self.move()
            self.turns += 1
        self.report()

    def move(self):
        move = self.player.move()
        if move.move_type == "move":
            self.board.get(move.loc).run_actions("attacked")
        elif move.move_type == "quit":
            self.game_over = True
        else:
            raise Exception("Unknown move type '%s'" % move_type)

    def report(self):
        print("You scored %d points in %d turns" % (self.score, self.turns))

if __name__ == '__main__':
    game().play()
    
