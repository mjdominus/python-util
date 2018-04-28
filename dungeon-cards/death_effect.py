#!/usr/bin/python3

class death_effect():
    def __init__(self, kind, health):
        self.n = health
        self.kind = kind
        self.burning = False
        self.poisoned = False   # also brain zombie
        self.teleports = False  # tentacle monster
        
