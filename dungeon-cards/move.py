#!/usr/bin/python3

from loc import loc

class move():
    def __init__(self, move_type, new_loc=None):
        self.move_type = move_type
        self.loc = new_loc

    def __str__(self):
        if self.loc is None:
            return self.move_type
        else:
        	return "%s %s" % (self.move_type, str(self.loc))