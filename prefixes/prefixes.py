#!/usr/bin/python3

import fileinput
import re
import sys
from collections import defaultdict

def debug(*args):
    return
    print(*args, file=sys.stderr)

dict = {}

def is_word(s):
    return dict.get(s, False)

def prefixes(s):
    p = []
    for i in range(1, len(s)):
        p.append(s[0:i])
#    debug("Prefixes of %s: %s" % ( s,
#                                   ", ".join(p) ))
    return p

def filter(p, ls):
    r = []
#    debug("  filtering %s with %s" % (repr(ls), repr(p)))
    for i in ls:
        if p(i):
#            debug("    %s: yep" % i)
            r += [i]
#        else:
#            debug("    %s: nope" % i)
#    debug("  result: %s" % r)
    return r

def good_prefixes(s):
    return filter(is_word, prefixes(s))

def suffixes(s):
    p = []
    for i in range(1, len(s)-1):
        p.append(s[i:])
#    debug("Suffixes of %s: %s" % ( s,
#                                   ", ".join(p) ))
    return p

def looks_good(s):
    return len(word) > 1 and re.fullmatch(r'[a-z]+', s)

#####

for word in fileinput.input():
    word = word.rstrip()
    if looks_good(word):
        dict.setdefault(word, True)

debug("Read %d words" % len(dict))

prefix_of = defaultdict(list)
suffix_of = defaultdict(list)
num_good_prefixes = defaultdict(int)

for word in list(dict.keys()):
    for prefix in good_prefixes(word):
#        debug("found good prefix %s of word %s" % (prefix, word))
        prefix_of[prefix] += [word]
        num_good_prefixes[word] += 1
    for suffix in suffixes(word):
        suffix_of[suffix] += [word]

# debug("prefixes: %s" % repr(prefix_of))

# for (prefix, wordlist) in list(prefix_of.items()):
#    print("%s: %s" % (prefix, ", ".join(list(wordlist))))

def replace(target, this, that):
    return that + target[len(this):]

# does string a start with string b?
def startswith(a, b):
    if len(a) < len(b): return False
    return a[0:len(b)] == b

# does string a end with string b?
def endswith(a, b):
    if len(a) < len(b): return False
    return a[len(a)-len(b) : ] == b

def remove_prefix(target, prefix):
    if startswith(target, prefix):
        return target[len(prefix):]
    else:
        raise ValueError("Can't remove prefix '%s' from '%s'" % (prefix, target))

def remove_suffix(target, suffix):
    if endswith(target, suffix):
        return target[: len(target) - len(suffix)]
    else:
        raise ValueError("Can't remove suffix '%s' from '%s'" % (suffix, target))


def win(pqs, pq, x, p, y):
#    print("In '%s':\n\treplacing '%s' with '%s' gives '%s'\n\treplacing '%s' with '%s' gives '%s'"
    print("%s: [%s -> %s] %s; [%s -> %s] %s"
      % (pqs,
         pq, x, replace(pqs, pq, x),
         p,  y, replace(pqs, p,  y)))
    win.wincount += 1
    if win.wincount % 10000 == 0: print("* ", win.wincount, file=sys.stderr)
win.wincount = 0

def is_boring_suffix(s):
    for ss in ['iest', 'ness', 'tion', 'tions', 'able', 'ally', 'some', 'ment', 'ists', 'ities', 'ized', 'izes', 'izing', 'ments', 'ingly', 'sion', 'sions', 'ing']:
        if endswith(s, ss): return True
    return False

interesting = defaultdict(int)
count = 0

for word in sorted(dict.keys()):
    gp = good_prefixes(word)
    if len(gp) < 2: continue
    debug("word '%s' has good prefixes '%s'" % (word, repr(gp)))
    winners = defaultdict(list)
    
    for p in gp:
        s = remove_prefix(word, p)
        if len(s) < 4: continue
        if is_boring_suffix(s): continue
        debug("  %s is a suffix of: %s" % (s, suffix_of[s]))
            
        if len(suffix_of[s]) > 1:
            for xs in suffix_of[s]:
                if xs == word: continue
                x = remove_suffix(xs, s)
                if re.match(r's$', p) and re.match(r's$', x): continue
                if len(x) < 4: continue
                if not is_word(x): continue
                winners[p] += [x]

        if len(winners.keys()) > 1:
            print("** %s" % word)
            for p in sorted(winners.keys()):
                for x in sorted(winners[p]):
                    print("   [ %-10s -> %-10s ] %-20s" %
                          ( p, x, replace(word, p, x) ))
