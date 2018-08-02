#!/usr/bin/python3
#
# Given N, generate all vectors v such that
#
#   sum i * v[i]   =   N
#

def all_patterns(N):
    yield from vec(N, N)

def vec(N, max_i):
    """max_i is the size of the largest nonzero vector element."""
    if max_i == N: yield ([0] * (max_i-1)) + [1]
    if max_i < N:
      for seq in vec(N-max_i, max_i):
          force_inc(seq, max_i-1) # -1 because of base-1 indexing
          yield seq
    if max_i > 1: yield from vec(N, max_i-1)
    return


# pad seq with zeroes until seq[i] exists, then increment seq[i]
# There must be a better way to do this
def force_inc(seq, i):
    while i not in range(len(seq)):
        seq += [0]
    seq[i] += 1

from sys import argv, stderr
if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage: pattern N", file=stderr)
        exit(2)
        
    for s in all_patterns(int(argv[1])):
        print(s)

        
