#!/usr/bin/python3

config = { "r": 100,            # medallion radius pixels
           "pr": 6,             # dot radius pixels
           "bgcolor": "white",
           "dotcolor": "purple",
           "linecolor": "darkblue",
           "xspc": 20,
           "yspc": 20,
           "nx": 6,             # number of medallions per row
           "pgw": 816,          # page width in pixels
           "pgh": 1056,         # page height
}

from math import cos, sin, pi, ceil
import sys

def cis(r, th):
    return (r * cos(th), r * sin(th))

class FullPage(Exception):
    pass

class pages():
    def __init__(self, config):
        self.config = config
        self.pages = []
        self.cur_page = None

    def add(self, medallion):
        if self.cur_page is None:
            self.new_page()

        try:
            self.cur_page.add(medallion)
        except FullPage:
            self.new_page().add(medallion)

    def new_page(self):
        new_page = page(self.config)
        self.pages.append(new_page)
        self.cur_page = new_page
        return new_page

    def render(self):
        for p in self.pages:
            p.render()
        return self

    def print(self, fp="page{:02d}.svg"):
        for i in range(len(self.pages)):
            p = self.pages[i]
            with open(fp.format(i), "w") as fh:
                for line in p.output:
                    print(line, file=fh)

class page():
    def __init__(self, config):
        self.config = config
        self.cur_x = 0
        self.cur_y = 0
        self.row_height = 0
        self.medallions = []

    def add(self, medallion):
        w = medallion.w()
        h = medallion.h()
        self.row_height = max(h, self.row_height)
        if self.cur_x + w > self.config["pgw"]: # start a new row
            self.cur_x = 0
            self.cur_y += self.row_height + self.config["yspc"]
            if self.cur_y + h > self.config["pgh"]: # page is full
                raise FullPage()
            self.row_height = h

        medallion.set_pos(self.cur_x, self.cur_y)
        self.cur_x += self.config["xspc"] + w
        self.medallions.append(medallion)

    def w(self): return self.config["pgw"]
    def h(self): return self.config["pgh"]

    def render(self):
        self.output = [ f'<svg viewBox="{0} {0} {self.w()} {self.h()}" xmlns="http://www.w3.org/2000/svg">' ]
        for m in self.medallions:
            ox, oy = m.pos
            self.output += [ f'<g transform="translate({ox} {oy})">' ] + m.render() + [ "</g>" ]
        self.output += [ '</svg>' ]
        return self.output

    def set_bounds(self):
        m = self.medallions[0]
        cols = self.config["nx"]
        rows = ceil(len(self.medallions) / cols)
        print(f"{rows} rows {cols} cols")
        self.w = cols * (m.w() + self.config["xspc"])
        self.h = rows * (m.h() + self.config["yspc"]) + self.config["yspc"]
        self.y0 = m.h() / 2 + self.config["yspc"]
        self.x0 = m.w() / 2 + self.config["xspc"]

    def print(self, fh):
        print(*self.output, file=fh)
        return self

class medallion():
    def __init__(self, perm, config):
        self.N = len(perm)
        self.perm = perm
        self.config = config
        self.init_points()
        self.output = []
        self.pos = (0,0)

    def init_points(self):
        p = []
        for i in range(self.N):
            theta = 2*pi*i/self.N
            p.append(cis(self.config["r"], theta))
        self.p = p

    def set_pos(self, x, y):
        self.pos = (x, y)

    def w(self):
        return self.config["r"] * 2

    def h(self):
        return self.config["r"] * 2

    def render_point(self, i):
        (x, y) = self.p[i]
        self.output.append(f'<circle cx="{x}" cy="{y}" r="{self.config["pr"]}" stroke-width="3" stroke="{self.config["bgcolor"]}" fill="{self.config["dotcolor"]}"/>')

    def render_line(self, i, j):
        (x1, y1) = self.p[i]
        (x2, y2) = self.p[j]
        self.output.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{self.config["linecolor"]}" stroke-linecap="round"/>')

    def render_background(self):
        r = self.config["r"]
        self.output.append(f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{self.config["bgcolor"]}" />')
#        self.output.append(f'<circle cx="0" cy="0" r="{r}" fill="none" stroke-width="1" stroke="rgb(13,13,13)" />')

    def render(self):
        r = self.config["r"]
        self.output = [ f'<g transform="translate({r} {r})">' ]
        self.render_background()
        for i in range(self.N):
            self.render_line(self.perm[i], self.perm[(i+1) % self.N])
        for i in range(self.N):
            self.render_point(i)
        return self.output + [ "</g>" ]

    def print(self, fh=sys.stdout):
        for s in self.output:
            print(s, file=fh)
        return self

def fact(n):
    f = 1
    while n > 0:
        f *= n
        n -= 1
    return f

def permutations(ls):
    i = 0
    N = len(ls)
    max = fact(N)
    while i < max:
        ii = i
        p = []
        q = ls.copy()
        for j in range(N, 0, -1):
            p.append(q.pop(ii % j))
            ii = int(ii / j)
        yield p
        i += 1

def one_cycle(p):
    return True
    i = p[0]
    c = 1
    while i != 0:
        i = p[i]
        c += 1
    return c == len(p)

def necklace(p):
    N = len(p)
    for k in range(N):
        for i in range(N):
            yield [ (j+k)%N for j in p[i:] + p[0:i] ]
    return

def bracelet(p):
    q = p.copy()
    q.reverse()
    yield from necklace(p)
    yield from necklace(q)

def rev(p):
    N = len(p)
    return [ 0 if i == 0 else N-i for i in p ]

def do_all(N):
    pg = pages(config)
    seen = set()
    for p in permutations(list(range(N))):
        if not one_cycle(p): continue
        skip = False
        for q in bracelet(p):
            if tuple(q) in seen or tuple(rev(q)) in seen:
                skip = True
                break
        if not skip:
            pg.add(medallion(p, config))
            seen.add(tuple(p))
    print(seen)
    pg.render().print()

if __name__ == '__main__':
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: medal.py N", file=sys.stderr)
        exit(2)

    if len(sys.argv) == 3:
        config["nx"] = int(sys.argv[2])

    config["r"] = int((4 * config["pgw"]) / (9*config["nx"]-1))
    config["xspc"] = int(config["r"] / 4)
    config["yspc"] = int(config["r"] / 4)
    print(f'nx={config["nx"]} r={config["r"]} spc={config["xspc"]}')
    print(f'  width={config["nx"] * 2 * config["r"] + (config["nx"] - 1) * config["xspc"] }')
    do_all(int(sys.argv[1]))
