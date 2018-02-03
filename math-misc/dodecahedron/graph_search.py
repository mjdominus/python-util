#!/usr/bin/python3

from sys import stderr

class graph:

    """Simple nondirected graphs.  Vertices are named
    with **positive** numbers 1...n"""
    
    def __init__(self, adj, expected_neighbors=None):
        """adj: adjacency information about the graph.
           adj[n] is a list of the vertices that are adjacent to
           vertex n.
           adj[0] is **unused**

        expected_neighbors: If the graph is uniform, this is the
        degree of every vertex.  (default: None)
        """
    
        self.adj = adj
        self.n_vertices = len(adj)-1
        self.expected_neighbors = expected_neighbors
        self.vertices = range(1, len(adj))
        
    def neighbors(self, v):
        """Neighbors of vertex v"""
        return self.adj[v]

    def adjacent(self, p, q):
        """Is vertex p adjacent to vertex q?"""
        return q in self.neighbors(p)

    def check(self):
        """Sanity check adjacency information:
           1. Is the relation symmetric?
           2. If the graph is uniform, are the neighbor lists the correct lengths?
        """
        ok = True
        for v in self.vertices:
            if (self.expected_neighbors is not None
                and len(self.neighbors(v)) != self.expected_neighbors):
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

dodecahedron = graph(
    [ "ooops",
            [ 2, 5, 6 ],  [ 1, 3, 8 ],  [2, 4,  10 ], # 1 2 3
            [ 3, 5, 12 ], [ 1, 4, 14 ], [1, 7,  15 ], # 4 5 6
            [ 6, 8, 18 ], [ 2, 7, 9 ],  [8, 10, 19],  # 7 8 9
            [ 3, 9, 11 ], [ 10, 12, 20 ], [ 4, 11, 13], # 10 11 12
            [ 12, 14, 16 ], [ 5, 13, 15 ], [ 6, 14, 17 ], # 13 14 15
            [ 13, 17, 20 ], [ 15, 16, 18 ], [ 7, 17, 19 ], # 16 17 18
            [ 9, 18, 20 ], [ 11, 16, 19],                  # 19 20
    ],
    expected_neighbors = 3)

if not dodecahedron.check():
    print("dodecahedron not ok")
    exit(1)

square =  graph([ "oops", [ 2, 4 ], [ 1, 3 ], [ 2, 4 ], [ 1, 3 ] ],
                expected_neighbors = 2)

if not square.check():
        print("square not ok")
        exit(1)

class graph_search:
    def __init__(self, g):
        """Find all the paths in the given graph."""
        self.g = g
    
    def paths(self,
              source, dest, used=[], maxlen=None,
              simple=True):
        """Each element in this sequence is a path from source to dest.
        A path is just a list of vertices.

        Keyword arguments:
        maxlen -- Maximum number of edges in the paths.
                  (default: equal to the number of vertices
                   in the graph.)
        simple -- Return simple paths only (default: True)
        (Simple paths use each vertex at most once.)

        used   -- List of vertices to avoid (default: [])
        """

        g = self.g
        if maxlen is None:
            maxlen = g.n_vertices

        if source == dest:
            yield [ source ];

        if maxlen == 0:
            return

        for next_vertex in [ v for v in g.neighbors(source)
                             if not (simple and v in used) ]:
            for partial_path in self.paths(next_vertex, dest,
                                           used=[*used, source],
                                           maxlen=maxlen-1,
                                           simple=simple):
                yield [ source, *partial_path ]
        return;

from collections import defaultdict

if __name__ == '__main__':
    count = defaultdict(int)
    total = 0
    for path in graph_search(dodecahedron).paths(1, 20, maxlen = 12, simple=False):
        print(path)
        count[len(path)-1] += 1
        total += 1
    for i in sorted(list(count.keys())):
        print("%3d %8d" % (i, count[i]))
    print("Total", total)
    
