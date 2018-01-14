#!/usr/bin/python3

from sys import stdin
from orthogon import svg_drawing

def draw_orthogon(file, args):
    draw = svg_drawing()
    for arg in args:
        if arg.startswith("r"):
            draw.right()
        elif arg.startswith("l"):
            draw.left()
        elif arg.startswith("f"):
            draw.step()
        else: raise Exception("Unknown instruction '%s' in line '%s'" % (arg. file))
        
    draw.file = open(file, mode="w")
    draw.output()
    draw.file.close()
    
if __name__ == '__main__':
    for line in stdin:
       fields = line.split()
       if len(fields) == 0: continue
       filename = fields[0] + ".svg"
       instructions = fields[1:]
       draw_orthogon(filename, instructions)

       

