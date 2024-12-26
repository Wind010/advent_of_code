'''
https://adventofcode.com/
'''



import re
from common.common import arg_parse, assertions, timer
from collections import Counter
from itertools import product


def parse_input(lines):
    locks, keys = [],[]
    for grid in lines:
        grid = grid.split('\n')
        if set(grid[0]) == set('#'):
            locks.append(get_counts(grid, True))
        else:
            keys.append(get_counts(grid, False))
        #print(locks, keys)
    return locks, keys


def get_counts(grid, is_lock):
    counts, rows, cols = [], len(grid), len(grid[0])
    for c in range(cols):
        count = -1
        for r in range(rows):
            v = grid[r][c]
            if is_lock and v == '#':
                count += 1
            if not is_lock and v == '#':
                count += 1
        counts.append(count)
    return tuple(counts)


def parse_input_transpose(lines):
    locks, keys = [],[]
    for grid in lines:
        grid = grid.split('\n')
        is_lock = set(grid[0]) == set('#')
        #transposed = [[row[i] for row in grid] for i in range(len(grid[0]))]
        transposed = [*zip(*grid)]
        
        lock, key = [], []
        for row in transposed:
            if is_lock:
                lock.append(Counter(row)['#'] - 1)
            else:
                key.append(Counter(row)['#'] - 1)
        
        if is_lock:
            locks.append(tuple(lock))
        else:
            keys.append(tuple(key))

    #print(locks, keys)
    return locks, keys


@timer
def find_key_lock_pairs(lines):
    locks, keys = parse_input(lines)
    fits = set()
    for lock, key in product(locks, keys):
        fits_pair = True
        for l, k in zip(lock, key):
            if l + k >= 6:
                fits_pair = False
                break
        
        if fits_pair:
            fits.add((lock, key))
        
        #if all(l + k < 6 for l, k in zip(lock, key)):
        #    fits.add((lock, key))
    return fits



def main(args, data):
    lines = data.strip().split('\n\n')

    pair_count = len(find_key_lock_pairs(lines))

    assertions(args, pair_count, 3, 3451, 3021)
    return pair_count
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)

