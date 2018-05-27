#!/usr/bin/python3
#
# Some sort of per-turn action

import filter

# abstract
class action():
    def __init__(self, game):
        self.g = game

    def run(self, card):
        raise Exception("Abstract action can't be run")

# I'm on fire, lose 1 health or cancel myself
class burn(action):
    def __init__(self):
        pass
    def run(self, card, atype):
        if card.h == 1:
            card.remove_action(atype, self)
        else:
            card.h -= 1

# This is what happens to a tree card
# when it is hist with a flame trap
class catch_fire(action):
    def __init__(self):
        pass
    def run(self, card, atype):
        card.add_action("turn", action.action_burn())

# Tentacle card teleport
class move(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        locations = filter(card.location().neighbors(),
                           lambda loc : not card.g.board.contents(loc).kind_is("player"))
        new_loc = card.g.random.select(locations)
        card.g.board.swap(card.loc, new_loc)

class player_move(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        new_loc = card.g.get_player_move()
        card.g.board.move_player(new_loc)

# Bomb counts down by 1
class tick(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        card.attr["tick"] -= 1
        if card.atttr["tick"] == 0:
            card.run_actions("tick0")

# Goblin steals adjacent gold (how much??)
class steal(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        locations = filter(card.location().neighbors(),
                           lambda loc : not card.g.board.contents(loc).kind_is("gold"))
        if locations:
            gold_loc = card.g.random.select(locations)
            gold = card.g.board.get(gold_loc)
            amount_stolen = card.g.random.amount(1, gold.h)
            gold.hit(amount_stolen)
            card.attr["sack"] += amount_stolen

# Gold is stolen-from by goblin
class stolen(action):
    def __init__(self):
        pass

    def run(self, card, atype, amount):
        card.h -= amount
        if card.h == 0:
            card.replace_with("empty", 0)

# This is a card informing us that the player is moving into our square
class card_attacked(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        player = card.g.player
        weapon = player.weapon
        attack = weapon.strength if weapon else card.g.player.h
        defense = card.h
        points = attack if attack < defense else defense
        if weapon:
            weapon.damage(points)
        else:
            card.g.player.damage(points)
        card.damage(points)
        if card.h == 0:
            # dead
            if weapon:
                card.replace_with_gold()
            else:
                raise Exception("unimplemented")

class card_snuffed(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        card.g.board.snuff_me(self)

class simple_coin(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        card.g.score += 1
        card.g.board.snuff_me(card)

class simple_trap(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        card.g.player_card.wound(1)
        card.g.board.snuff_me(card)

import action