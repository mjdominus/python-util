#!/usr/bin/python3

import board
import player

class game():
    def __init__(self):
        self.b = board()
        self.rand = None   # actually prompts terminal for result
        self.player = player()
