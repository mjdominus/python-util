#!/usr/bin/python3

import random as r

class random():
    def __init__(self):
        pass

    def rand_item(self, ls):
        r = r.randrange(len(ls))
        return ls[r]

    def true_random(self, mx):
        return r.randrange(mx)


