import numpy as np

def _2_to_1(column, row):
    """
    Translate 2 dims param into 1 dim.
    
        row   index (result)          pascal's triangle
    col     0  1  2  3  4  5
         0  0  -  -  -  -  -        1
         1  1  2  -  -  -  -        1  1
         2  3  4  5  -  -  -        1  2  1
         3  6  7  8  9  -  -        1  3  3  1
         4  10 11 12 13 14 -        1  4  6  4  1
         5  15 16 17 18 19 20       1  5  10 10 5  1
            ...6

    """
    #assert column <= row, 'Column cannot be larger than rows'
    if column > row or column < 0:
        return 0
    return int(row*(row+1)/2) + column

def pascals_triangle(column, row):
    """
    Basic implementation for Pascal's Triangle.
    Absence of cached results in poor performance for large column and row.

    :c column:
    :r row:
    :p pascal's triangle number:
    """
    def pascals_rec(c, r):
        if c == 0 or c == r:
            return 1
        else:
            return pascals_rec(c-1, r-1) + pascals_rec(c, r-1)
    return pascals_rec(column, row)

def build_cache(cache_width=10, cache_height=10):

    cache_size = _2_to_1(cache_width, cache_height)
    cache_impl = np.zeros((cache_size,), dtype=np.uint16)

    cache_impl[_2_to_1(0,0)] = 1
    cache_impl[_2_to_1(0,1)] = 1
    cache_impl[_2_to_1(1,1)] = 1
    cache_impl[_2_to_1(0,2)] = 1
    cache_impl[_2_to_1(1,2)] = 2
    cache_impl[_2_to_1(2,2)] = 1

    for r in range(3, cache_height):
        for c in range(0, r+1):

            top_left = _2_to_1(c-1,r-1)
            top = _2_to_1(c,r-1)

            value_top_left = cache_impl[top_left]
            value_top = cache_impl[top]
            if top_left == 0:
                value_top_left = 0

            print(_2_to_1(c, r), value_top_left, value_top)

            #print(c, r, _2_to_1(c, r), ':', c, r-1, _2_to_1(c, r-1), ':', c-1, r-1, _2_to_1(c-1, r-1))
            #print(_2_to_1(c, r), ':', cache_impl[_2_to_1(c, r-1)], ':', cache_impl[_2_to_1(c-1,r-1)])
            cache_impl[_2_to_1(c, r)] = value_top_left + value_top
            #if top_left != 0 and top != 0:
            #    cache_impl[_2_to_1(c,r)] = cache_impl[_2_to_1(c-1,r-1)] + cache_impl[_2_to_1(c,r-1)]
            #    print('uhuy')
    print(cache_impl)

build_cache(5, 5)