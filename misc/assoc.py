#!/usr/bin/python3
#
# Thing that thinks about a category
# and can check it to see if its composition
# is associative

import itertools
import sys

class Category():
    def __init__(self, morphisms=None, compositions=None):
        if morphisms is None:
            morphisms = {}      # maps names to morphism objects
        self.morphisms = morphisms
        if compositions is None:
            compositions = {}   # maps name pairs to morphism objects
        self.compositions = compositions
        for m in self.morphisms.values():
            self.add_identities(m)

    def morphism_names(self):
        return self.morphisms.keys()

    def add_identities(self, m):
        self.add_identity(m.source)
        self.add_identity(m.target)

    def add_identity(self, obj):
        id_name = f"id_{obj}"
        if id_name not in self.morphisms:
            self.add_morphism(Morphism(obj, obj, name=id_name))

    def add_morphisms(self, ms):
        for m in ms:
            self.add_morphism(m)
        return self

    def add_morphism(self, m):
        name = m.name
        print("Adding", name)
        if name in self.morphisms:
            if m is not self.morphisms[name]:
                raise Exception(f"Conflicting name {name}")
        else:
            self.morphisms[name] = m
        self.add_identities(m)
        return self

    def compose(self, first, second):
        if not first.composable(second):
            raise Exception(f"{second.name} ∘ {first.name} can't be composed")

        if first.is_identity(): return second
        elif second.is_identity(): return first

        pair = (first.name, second.name)
        if pair not in self.compositions:
            self.compositions[pair] = self.get_composition(first, second)

        return self.compositions[pair]

    def get_composition(self, first, second):
        print(f"Compose {second} ∘ {first} : {first.source} → {second.target}")
        name = sys.stdin.readline().rstrip()
        if name in self.morphisms:
            a = self.morphisms[name]
            if a.source != first.source:
                raise Exception(f"Bad source (need {first.source}, got {a.source})")
            elif a.target != second.target:
                raise Exception(f"Bad target (need {second.target}, got {a.target})")
        else:
            self.morphisms[name] = Morphism(first.source, second.target, name=name)
        return  self.morphisms[name]

    def check_associativity(self):
        checked = set()
        new_check_needed = True

        while new_check_needed:
            new_check_needed = False
            for trip in itertools.product(self.morphism_names(), repeat=3):
                a, b, c = (self.morphisms[name] for name in trip)
                print(trip)
                if not a.composable(b) or not b.composable(c):
                    continue
                if trip in checked:
                    continue
                new_check_needed = True
                lt = self.compose(self.compose(a, b), c)
                rt = self.compose(a, self.compose(b, c))
                if lt is not rt:
                    raise Exception(f'{left}\n = ({a} ∘ {b}) ∘ {c}\n ≠ {a} ∘ ({b} ∘ {c})\n = {right}')
                checked.add(trip)

        print(f"Checked {len(checked)} triples:", checked)
        return True

class Morphism():
    _next_name = ord("D")

    def __init__(self, source, target, compositions=None, name=None):
        if name is None:
            name = self.make_name()
        self.name = name
        self.source = source
        self.target = target

    def __str__(self):
        return self.name

    def desc(self):
        return f"{self} : {self.source} → {self.target}"

    def make_name(self):
        name = chr(_next_name)
        _next_name += 1
        return name

    def is_identity(self):
        return self.name.startswith("id_")

    def composable(self, follower):
        return self.target == follower.source

m = ( Morphism("1", "B", name="x"),
      Morphism("1", "B", name="y"),
      Morphism("A", "1", name="!A"),
      Morphism("A", "B", name="!"),
      )

C = Category().add_morphisms(m).check_associativity()
