#!/usr/bin/python3

import death_effect
from game import GAME

# Includes: player, bomb, pickup, etc.

class monster():
    def __init__(self, kind, health, location):
        self.h = health
        self.attr = {} # tick is bomb tick count; sack is goblin sack contents
        self.kind = kind
        self.loc = location
        self.actions = { "turn": [],  # Does this every turn
                         "death": [],  # Does this when it dies
                         "attacked": [],    # Does this when attacked
                         "flamed": [], # Does this when burnt
                         "poisoned": [], # Does this when poisoned
                         "tick0": [], # Does this when times runs out
        }

    def remove_action(self, action_type, action):
        self.actions[action_type].remove(action)

    def add_action(self, action_type, action):
        self.actions[action_type].append(action)

    def run_actions(self, action_type):
        for action in self.actions[action_type]:
            action.run(self, action_type)
            
    def kind_is(self, what):
        return self.kind == what

    def moved(self, loc):
        self.loc = loc

    def replace_with(self, kind, health):
        loc = self.loc
        new = monster(kind, health, location=None)
        GAME.board.set(loc, new)
