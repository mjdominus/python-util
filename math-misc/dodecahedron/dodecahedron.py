#!/usr/bin/python3

from sys import stderr

class dodecahedron:
    n_vertices = 20
    dodecahedron = [ "ooops",
            [ 2, 5, 6 ],  [ 1, 3, 8 ],  [2, 4,  10 ], # 1 2 3
            [ 3, 5, 12 ], [ 1, 4, 14 ], [1, 7,  15 ], # 4 5 6
            [ 6, 8, 18 ], [ 2, 7, 9 ],  [8, 10, 19],  # 7 8 9
            [ 3, 9, 11 ], [ 10, 12, 20 ], [ 4, 11, 13], # 10 11 12
            [ 12, 14, 16 ], [ 5, 13, 15 ], [ 6, 14, 17 ], # 13 14 15
            [ 13, 17, 20 ], [ 15, 16, 18 ], [ 7, 17, 19 ], # 16 17 18
            [ 9, 18, 20 ], [ 11, 16, 19],                  # 19 20
    ]
    expected_neighbors = 3
    adj = dodecahedron

    n_vertices = 4
    square = [ "oops", [ 2, 4 ], [ 1, 3 ], [ 2, 4 ], [ 1, 3 ] ]
    expected_neighbors = 2
    adj = square

    vertices = range(1,n_vertices + 1)

    @classmethod
    def neighbors(self, v):
        return self.adj[v]

    @classmethod
    def adjacent(self, p, q):
        return q in self.neighbors(p)

    @classmethod
    def check(self):
        ok = True
        for v in self.vertices:
            if len(self.neighbors(v)) != self.expected_neighbors:
                print("vertex %d has %d neighbors!" % (v, len(self.neighbors(v))),
                      file=stderr)
                ok = False
            for n in self.neighbors(v):
                if not self.adjacent(v, n):
                    print("vertex %d not adjacent to %d, WTF!" % (v, n),
                          file=stderr)
                    ok = False
                if not self.adjacent(n, v):
                    print("asymmetry: vertex %d not adjacent to %d" % (n, v),
                          file=stderr)
                    ok = False
        return ok

    @classmethod
    def paths(self,
              source, dest, used=[], maxlen=None,
              simple=True):
        if maxlen is None:
            maxlen = self.n_vertices

        if source == dest:
            yield [ source ];

        if maxlen == 0:
            return

        for next_vertex in [ v for v in self.neighbors(source)
                             if not (simple and v in used) ]:
            for partial_path in self.paths(next_vertex, dest,
                                           used=[*used, source],
                                           maxlen=maxlen-1,
                                           simple=simple):
                yield [ source, *partial_path ]
        return;

if __name__ == '__main__':
    if not dodecahedron.check():
        print("not ok")
        exit(1)
    count = []
    total = 0
    for path in dodecahedron.paths(1, 3, maxlen = 6, simple=False):
        print(path)
        ln = len(path)-1
        while (len(count) < ln+1):
            count.append(0)
        count[ln] += 1
        total += 1
        if total % 1000000 == 0:
            print("*", total * 100 / 86367288.0, file=stderr)
    for i in range(len(count)):
        if count[i] > 0:
            print("%3d %4d" % (i, count[i]))
    print("Total", total)
