#!/usr/bin/python3
#
# Some sort of per-turn action

import filter
from game import GAME

# abstract
class action():
    def __init__(self):
        pass

    def run(self, card):
        raise Exception("Abstract action can't be run")

# I'm on fire, lose 1 health or cancel myself
class action_burn(action):
    def __init__(self):
        pass
    def run(self, card, atype):
        if card.h == 1:
            card.remove_action(atype, self)
        else:
            card.h -= 1

# This is what happens to a tree card
# when it is hist with a flame trap
class action_catch_fire(action):
    def __init__(self):
        pass
    def run(self, card, atype):
        card.add_action("turn", action_burn())
    
# Tentacle card teleport
class action_move(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        locations = filter(card.location().neighbors(),
                           lambda loc : not GAME.board.contents(loc).kind_is("player"))
        new_loc = GAME.random.select(locations)
        GAME.board.swap(card.loc, new_loc)
        
class action_player_move(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        new_loc = GAME.get_player_move()
        GAME.board.move_player(new_loc)

# Bomb counts down by 1        
class action_tick(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        card.attr["tick"] -= 1
        if card.atttr["tick"] == 0:
            card.run_actions("tick0")

# Goblin steals adjacent gold (how much??)
class action_steal(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        locations = filter(card.location().neighbors(),
                           lambda loc : not GAME.board.contents(loc).kind_is("gold"))
        if locations:
            gold_loc = GAME.random.select(locations)
            gold = GAME.board.get(gold_loc)
            amount_stolen = GAME.random.amount(1, gold.h)
            gold.hit(amount)
            card.attr["sack"] += amount

# Gold is stolen-from by goblin
class action_stolen(action):
    def __init__(self):
        pass

    def run(self, card, atype, amount=n):
        card.h -= n
        if card.h == 0:
            card.replace_with("empty", 0)

# This is a card informing us that the player is moving into our square
class action_card_attacked(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        player = GAME.player
        weapon = player.weapon
        attack = weapon.strength if weapon else GAME.player.h
        defense = card.h
        points = attack if attack < defense else defense
        if weapon:
            weapon.damage(points)
        else:
            GAME.player.damage(points)
        card.damage(points)
        if card.h == 0:
            # dead
            if weapon:
                card.replace_with_gold()
            else:
                ... ??

class action_card_snuffed(action):
    def __init__(self):
        pass

    def run(self, card, atype, amount=n):
        pass
            
class action_simple_coin(action):
    def __init__(self):
        pass

    def run(self, card, atype):
        GAME.score += 1
        GAME.board.snuff(card)
        
    
