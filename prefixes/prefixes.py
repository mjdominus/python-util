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
    

interesting = defaultdict(int)
count = 0

for pqs in dict.keys():
    if endswith(pqs, 'ness'): continue
    gp = good_prefixes(pqs)
    debug("word '%s' has good prefixes '%s'" % (pqs, repr(gp)))
    for i in range(len(gp)-1):
        p = gp[i]
        for j in range(i+1, len(gp)):
            pq = gp[j]
            q = remove_prefix(pq, p)
            s = remove_prefix(pqs, pq)
            qs = remove_prefix(pqs, p)

            if len(s) < 3: continue
            if len(p) < 4: continue
            if len(q) < 2: continue
            
            debug(repr(['pqs', pqs, 'pq', pq, 'q', q,
                        's', s, 'qs', qs]))

            debug("  %s is a suffix of: %s" % (qs, suffix_of[qs]))
            debug("  %s is a suffix of: %s" % (s,  suffix_of[s]))
            
            if len(suffix_of[qs]) > 1 and len(suffix_of[s]) > 1:
                for xqs in suffix_of[qs]:
                    if xqs == pqs: continue
                    debug("  trying '%s' which has suffix '%s'"
                          % (xqs, qs))
                    x = remove_suffix(xqs, qs)
                    if not is_word(x): continue
                    winners = []
                    for ys in suffix_of[s]:
                        if ys == pqs: continue
                        if ys == xqs: continue
                        y = remove_suffix(ys, s)
                        if not is_word(y): continue
                        winners += [ (pq, y) ]
                    if len(winners) > 0:
                        win2(pqs, p, x, winners)
                        # win(pqs, p, x, pq, y)
                        # k = ",".join([pqs,p,pq])
                        # if k in interesting:
                        #     interesting[k] += 1
                        # else:
                        #     print("*  ", k)
                        #     interesting[k] = 1
                        # count += 1
                        # if count % 100000 == 0: print(count, file=sys.stderr)

for k in interesting.keys():
    print("%4d %-20s" % (interesting[k], k))
    
