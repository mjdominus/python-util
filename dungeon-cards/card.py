#!/usr/bin/python3

from cardtype import card_library

# Includes: monster, player, bomb, pickup, etc.

# TODO : distinguish card from cardtype
# kind and actions go into cardtype (I think)
# health and location go into card

class card():
    def __init__(self, game, kind, health, location=None):
        self.g = game
        self.h = health
        self.attr = {} # tick is bomb tick count; sack is goblin sack contents
        self.name = kind # cardtype object
        self.type = card_library[kind]
        self.loc = location

    def desc(self):
        return self.name + "(health %d)" % self.h

    def announce(self, *msgs):
      desc = self.desc()
      for msg in msgs:
          print(desc + ":", msg)

    def remove_action(self, action_type, action):
        self.name.actions[action_type].remove(action)

    def add_action(self, action_type, action):
        self.name.actions[action_type].append(action)

    def run_actions(self, action_type):
        self.announce("attacked")
        for action in self.type.actions[action_type]:
            action.run(self, action_type)
            
    def kind_is(self, what):
        return self.name == what

    def moved(self, loc):
      self.announce("moved to %s" % str(loc))
      self.loc = loc

    def replace_with(self, kind, health):
        loc = self.loc
        new = card(self.g, kind, health, location=None)
        self.g.board.set(loc, new)

    def wound(self, points):
      self.announce("wounded %d" % points)
      self.h -= points
      if points <= 0:
        self.run_actions("die")


