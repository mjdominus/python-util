
class Table(list):
    def __init__(self, spots):
        assert len(spots) == 3
        super().__init__(spots)
        assert len(self) == 3
        
    def appearance(self):
        return [ s[0] if s else None for s in self ]

    def __repr__(self):
        z = super().__repr__()
        return "T: " + z

    def copy(self):
        return Table(super().copy())

Any = "ANY"
Ace = "A"
Deuce = "2"
Three = "3"

all_tables = []
cardlists = [[Ace, Deuce, Three],
             [Ace, Three, Deuce],
             [Deuce, Ace, Three],
             [Deuce, Three, Ace],
             [Three, Ace, Deuce],
             [Three, Deuce, Ace]]

for cardlist in cardlists:
    for p1 in 0, 1, 2:
        for p2 in 0, 1, 2:
            for p3 in 0, 1, 2:
                table = [[], [], []]
                table[p1].append(cardlist[0])
                table[p2].append(cardlist[1])
                table[p3].append(cardlist[2])
                if table not in all_tables:
                    all_tables.append(Table(table))

#from pprint import pprint
#pprint(all_tables)
#for c in all_tables:
#    if len(c[0]) == 1 and len(c[2]) == 1:
#        pprint(c)

class Algorithm():
    def __init__(self):
        self.rules = []

    def add_rule(self, pattern, move):
        self.rules.append((pattern, move))

    def apply_rule(self, table):
        for r in self.rules:
            pattern, move = r
            if pattern.matches(table.appearance()):
                print(table, pattern, move, sep="\n")
                return move.apply(table)
        raise Exception("No matching rule")

    def test1(self, init):
        seen = []
        table = init
        print("-- testing", table)
        while table not in seen:
            seen.append(table)
            table = self.apply_rule(table)
            if self.victory(table):
                return True
        return seen

    def failure(self):
        for init in all_tables:
            if self.test1(init) is not True:
                return init
        return None

    def victory(self, table):
        for i in [0,1,2]:
            if len(table[i]) == 3:
                if table[i][0] == Ace and table[i][1] == Deuce:
                    return True
        return False

class Pattern():
    def __init__(self, p1, p2, p3, sliding=True):
        self.sub_patterns = [p1, p2, p3]
        self.sliding = sliding

    def __repr__(self):
        sp = self.sub_patterns
        return f"PAT{sp}"
                      
    def matches(self, appearance):
        if self.sliding:
            offsets = range(3)
        else:
            offsets = [0]
        for off in offsets:
            if self.matches_fixed(appearance):
                return True
            appearance = appearance[1:] + [ appearance[0] ]
        return False

    def matches_fixed(self, appearance):
        for c in zip(self.sub_patterns, appearance):
            if c[0] is Any:
                continue
            elif c[0] is None and c[1] is not None:
                return False
            elif c[0] != c[1]:
                return False
        return True

class Move():
    def __init__(self, find, direction):
        self.find = find
        self.direction = direction

    def __repr__(self):
        arrow = "←" if self.direction is "L" else "→"
        return f"MOVE {self.find} {arrow}"

    def apply(self, table):
        table = table.copy()
        found = False
#        import pdb; pdb.set_trace()
        for i in range(len(table)):
            if len(table[i]) == 0:
                continue
            if self.find is Any or table[i][0] == self.find:
                found = True
                break
        if not found:
            raise Exception(f"Couldn't find {self.find} in {table}")
        spot = table[i]
        top, rest = spot[0], spot[1:]
        table[i] = rest
        if self.direction is "R":
            i += 1
        elif self.direction is "L":
            i += 2
        else:
            raise Exception(f"Direction {self.direction}??")
            
        if i >= 3: i -= 3
        table[i] = [ top ] + table[i]
        return table

mine = Algorithm()
mine.add_rule(Pattern(Ace, Deuce, Three),
              Move(Deuce, "R"))
mine.add_rule(Pattern(Ace, Three, Deuce),
              Move(Deuce, "L"))

# If the ace is on the three, we will uncover it
# If the deuce is on the three, we will win
mine.add_rule(Pattern(Ace, Deuce, None),
              Move(Ace, "L"))
mine.add_rule(Pattern(Deuce, Ace, None),
              Move(Ace, "L"))

mine.add_rule(Pattern(Ace, Three, None),
              Move(Ace, "L"))
mine.add_rule(Pattern(Three, Ace, None),
              Move(Three, "L"))

mine.add_rule(Pattern(Deuce, Three, None),
              Move(Deuce, "L"))
mine.add_rule(Pattern(Three, Deuce, None),
              Move(Three, "L"))

mine.add_rule(Pattern(Any, None, None),
              Move(Any, "L"))

if __name__ == '__main__':
#    mine.test1(Table([[], [Three, Deuce], [Ace]]))
    z = mine.failure()
    if z is None:
        print("Victory!")
    else:
        print("Failed:", z)
