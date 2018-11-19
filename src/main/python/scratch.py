import numpy as np
from itertools import combinations_with_replacement


cache_row = 10
cache_impl = np.empty((cache_row*cache_row,), dtype=np.uint16)

def cache(c, r, w=False):
    if r <= 1:
        w = 1
    if w:
        cache_impl[r*c+c] = w
    return cache_impl[r*c+c]

def pascals_triangle(column, row):
    def pascals_rec(c, r):
        if c == 0 or c == r:
            return 1
        else:
            return pascals_rec(c-1, r-1) + pascals_rec(c, r-1)
    return pascals_rec(column, row)

def pascals_triangle_cached(column, row):
    def pascals_rec(c, r):
        if c == 0 or c == r:
            cache(0, 0, 1)
            cache(0, 1, 1)
            cache(1, 1, 1)
        else:
            return cache(c-1, r-1) + cache(c, r-1)
    return pascals_rec(column, row)


for r in range(cache_row):
    for c in range(r+1):
        cache(c, r, pascals_triangle_cached(c, r))

print(cache_impl)

def pascals_cache_builder(row, pascals_function):
    cache_length = int(row*(row+1)/2)
    cache = np.empty((cache_length,), dtype=np.uint8)
    counter = 0
    for r in range(row):
        for c in range(0, r+1):
            cache[counter] = pascals_function(c, r)
            counter = counter + 1
    def result(x, y):
        return cache[(y*x+x)+1]

    #return result
    return cache

# column 0 row 0 = 0
# column 0 row 1 = 1
# column 1 row 1 = 1
# column 0 row 2 = 1
# column 1 row 2 = 2
# column 2 row 2 = 1

#print(pascals_triangle(1,1))
#from_cache = pascals_cache_builder(10,pascals_triangle)
#print(from_cache)

def factorial(n, lower_bound=1):
    def factorial_rec(acc, r):
        if r <= lower_bound:
            return acc
        return factorial_rec(acc*r, r-1)
    return factorial_rec(1, n)

def combination(n, r, repeat=False):
    result = 0
    if not repeat:
        result = factorial(n, n-r)/factorial(r)
    else:
        result = factorial(r+n-1, n-1)/factorial(r)
    return int(result)

def combination_member(n, r):
    n = np.arange(n, dtype=np.uint8)
    return combinations_with_replacement(n,r)

distinct = lambda x: len(set(x))

def get_distinct(n, r, prob=True):
    keys = {}
    space = combination(n, r, prob)

    for i in map(distinct, combination_member(n,r)):
        result = keys.get(str(i), 0) + 1
        keys[str(i)] = result
    if prob:
        for key in keys:
            keys[key] = keys[key]/space
    return keys

def hypothesis(n, r, prob=True):
    keys = {}
    space = combination(n, r, prob)

    for i in range(1, r+1):
        #print("C({}, {}) = {}".format(n, r-i+1, combi))
        pi = pascals_triangle(i-1, r-1) # right..
        combi = combination(n, i) # hmm
        result = combi*pi
        #print("    {} * {} = {}".format(combi, pi, result))
        keys[str(i)] = int(result)
        if prob:
            keys[str(i)] = str("{:.4f}".format(result*1.0/space))
    return keys

#for x in range(1,500):
    #print(get_distinct(100, x))
    #print("35, {}".format(x))
#    print(hypothesis(1000, x))
    #print(get_distinct(35, x))
    #print()

