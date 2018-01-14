#!/usr/bin/python3

from sys import argv

class svg_drawing:
    offset = [ [1, 0], [0, 1], [-1, 0], [0, -1] ]
    def __init__(self, stepsize=50):
        self.heading = 0        # 0 = east, 1 = north
        self.x = 0
        self.y = 0
        self.stepsize = stepsize
        self.points = [[0, 0]]

    def step(self, n=1):
        self.x += self.stepsize * n * svg_drawing.offset[self.heading][0]
        self.y += self.stepsize * n * svg_drawing.offset[self.heading][1]
        self.points.append([self.x, self.y])

    def right(self):
        if self.heading == 0: self.heading = 3
        else:                 self.heading -= 1

    def left(self):
        if self.heading == 3: self.heading = 0
        else:                 self.heading += 1

    def output(self):
        self.output_header()

        coord_list = ""
        for p in self.points:
#            print("point: " + str(p))
            coord_list += str(p[0]) + "," + str(p[1]) + " "
        print("<polygon points = \"", coord_list, "\"/>")
            
        self.output_footer()

    def output_header(self):
        print("""
<svg xmlns='http://www.w3.org/2000/svg'
width="120" height="120" viewBox="0 0 120 120"
>
""")
        
    def output_footer(self):
        print("</svg>")
        
if __name__ == '__main__':
    draw = svg_drawing()
    for arg in argv[1:]:
        if arg.startswith("r"):
            draw.right()
        elif arg.startswith("l"):
            draw.left()
        elif arg.startswith("f"):
            draw.step()
        else: raise Exception("Unknown instruction '%s'" % arg)

    draw.output()

