#!/usr/bin/python3

from sys import argv, stdout

class svg_drawing:
    offset = [ [1, 0], [0, -1], [-1, 0], [0, 1] ]
    def __init__(self, stepsize=50, file=stdout):
        self.heading = 0        # 0 = east, 1 = north
        self.x = 0
        self.y = 0
        self.stepsize = stepsize
        self.points = [[0, 0]]
        self.xr = [0, 0]    # [min, max]
        self.yr = [0, 0]
        self.file = file

    def step(self, n=1):
        self.x += self.stepsize * n * svg_drawing.offset[self.heading][0]
        self.y += self.stepsize * n * svg_drawing.offset[self.heading][1]
        self.points.append([self.x, self.y])
        self.adjust_ranges()

    def adjust_ranges(self):
        self.xr[0] = min(self.xr[0], self.x)
        self.xr[1] = max(self.xr[1], self.x)
        self.yr[0] = min(self.yr[0], self.y)
        self.yr[1] = max(self.yr[1], self.y)

    def right(self):
        if self.heading == 0: self.heading = 3
        else:                 self.heading -= 1

    def left(self):
        if self.heading == 3: self.heading = 0
        else:                 self.heading += 1

    def output(self):
#        self.adjust_viewBox()
        self.output_header()

        coord_list = ""
        for p in self.points:
#            print("point: " + str(p))
            coord_list += str(p[0]) + "," + str(p[1]) + " "
        print("<polygon points = \"", coord_list, "\"/>", file=self.file)
            
        self.output_footer()

    def output_header(self):
        print("""
<svg xmlns='http://www.w3.org/2000/svg'
width="%d" height="%d" viewBox="%s"
>
"""
              % (self.width(), self.height(), self.viewBox()),
              file=self.file)
        
    def width(self):
        return self.xr[1] - self.xr[0]

    def height(self):
        return self.yr[1] - self.yr[0]

    def viewBox(self):
        return " ".join([str(n) for n in
                         [self.xr[0], self.yr[0],
                          self.width(), self.height()]])

    def output_footer(self):
        print("</svg>", file=self.file)
        
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

