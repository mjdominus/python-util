#!/usr/bin/python3

# All unordered multisets of size "size" whose members
# are drawn from "members"
class unordered_sets():
    def __init__(self, size, members):
        self.size = size
        self.members = members

    def __iter__(self):
        if self.size == 0:
            yield []
            return

        for i in range(len(self.members)):
            for j in unordered_sets(self.size-1, self.members[i:]):
                yield [self.members[i], *j]

class numset():
    def __init__(self, target, nums, subsize=None):
        self.nums = nums
        self.target = target
        self.subsize = numset.default(subsize, target)

    def __hash__(self):
        str(sorted(self.nums))
        
    def default(x, y):
        if x is None: return y
        else: return x

    def sum(nums):
        i = 0
        for num in nums: i += num
        return i

    def has_zero_sum(self, s):
        return sum(s) % self.target == 0
        
    def is_good(self):
        for s in subset_enumerator(self.nums, self.subsize):
            if self.has_zero_sum(s): return True
        return False

    def is_bad(self):
        return not self.is_good()

    def extend(self, n):
#        print(">> ", [*self.nums, n])
        a = [*self.nums, n]
        z = numset(self.target, [*self.nums, n], subsize=self.subsize)
        return z

    def __len__(self): return len(self.nums)
    
# for s in subset_enumerator([1,2,3,4,5], 3): ....

class subset_enumerator:
    def __init__(self, nset, osize):
        if len(nset) > 0:
            self.nset = nset[1:]
            self.first = nset[0]
        self.osize = osize

    def __iter__(self):
        if self.osize == 0:
            yield []
            return
        
        for sub in subset_enumerator(self.nset, self.osize-1):
            yield [self.first, *sub]

        if (self.osize <= len(self.nset)):
            for sub in subset_enumerator(self.nset, self.osize):
                yield sub
        return

class search():
    def __init__(self, d, items=None):
        if items is None: self.items = range(d)
        else: self.items = items

        self.target = d
        self.queue = list(unordered_sets(d, range(d)))
        self._maxsize = None
        self.seen = {}

    def find_bad(self, callback=None):
        self._maxsize = 0
        while len(self.queue) > 0:
            node = self.queue.pop()
            if self.already_saw(node): continue
            node_numset = numset(self.target, node)
            if node_numset.is_good(): continue
            if not callback is None and len(node) >= self._maxsize:
                callback(sorted(node))
            self._maxsize = max(self._maxsize, len(node))
            self.queue.extend([ node_numset.extend(i).nums for i in self.items ])

    def already_saw(self, node):
        key = str(sorted(node))
        if self.seen.get(key, None) is None:
            self.seen[key] = 1
            return False
        else:
            return True

    def maxsize(self):
        if self._maxsize is None:
            self.find_bad()
        return self._maxsize

    def print_bad(self):
        self.find_bad(callback=print)

d = 4
x = search(d)
x.print_bad()
print("n(%d) = %d"% (d, x.maxsize() + 1))
