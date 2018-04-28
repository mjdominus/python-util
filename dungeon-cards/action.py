#!/usr/bin/python3
#
# Some sort of per-turn action

import filter
from game import GAME

# abstract
class action():
    def __init__(self):
        pass

    def run(self, monster):
        raise Exception("Abstract action can't be run")
        
# I'm on fire, lose 1 health or cancel myself
class action_burn(action):
    def __init__(self):
        pass
    def run(self, monster, atype):
        if monster.h == 1:
            monster.remove_action(atype, self)
        else:
            monster.h -= 1

# This is what happens to a tree monster
# when it is hist with a flame trap
class action_catch_fire(action):
    def __init__(self):
        pass
    def run(self, monster, atype):
        monster.add_action("turn", action_burn())
    
# Tentacle monster teleport
class action_move(action):
    def __init__(self):
        pass

    def run(self, monster, atype):
        locations = filter(monster.location().neighbors(),
                           lambda loc : not GAME.board.contents(loc).kind_is("player"))
        new_loc = GAME.random.select(locations)
        GAME.board.swap(monster.loc, new_loc)
        
class action_player_move(action):
    def __init__(self):
        pass

    def run(self, monster, atype):
        new_loc = GAME.get_player_move()
        GAME.board.move_player(new_loc)

# Bomb counts down by 1        
class action_tick(action):
    def __init__(self):
        pass

    def run(self, monster, atype):
        monster.attr["tick"] -= 1
        if monster.atttr["tick"] == 0:
            monster.run_actions("tick0")

# Goblin steals adjacent gold (how much??)
class action_steal(action):
    def __init__(self):
        pass

    def run(self, monster, atype):
        locations = filter(monster.location().neighbors(),
                           lambda loc : not GAME.board.contents(loc).kind_is("gold"))
        if locations:
            gold_loc = GAME.random.select(locations)
            gold = GAME.board.get(gold_loc)
            amount_stolen = GAME.random.amount(1, gold.h)
            gold.hit(amount)
            monster.attr["sack"] += amount

# Gold is stolen-from by goblin
class action_stolen(action):
    def __init__(self):
        pass

    def run(self, monster, atype, amount=n):
        monster.h -= n
        if monster.h == 0:
            monster.replace_with("empty", 0)

# This is a monster informing us that the player is moving into our square
class action_monster_attacked(action):
    def __init__(self):
        pass

    def run(self, monster, atype):
        player = GAME.player
        weapon = player.weapon
        attack = weapon.strength if weapon else GAME.player.h
        defense = monster.h
        points = attack if attack < defense else defense
        if weapon:
            weapon.damage(points)
        else:
            GAME.player.damage(points)
        monster.damage(points)
        if monster.h == 0:
            # dead
            if weapon:
                monster.replace_with_gold()
            else:
                ... ??

class action_monster_snuffed(action):
    def __init__(self):
        pass

    def run(self, monster, atype, amount=n):
            
