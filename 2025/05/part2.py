'''
https://adventofcode.com/2025/day5
'''


from common.common import arg_parse, assertions, timer
from itertools import chain

import numpy as np



def get_fresh_ids(fresh_ranges):
    """Too slow"""
    fresh_ids = set()
    for r in fresh_ranges:
        fresh_ids.update(r)
    return list(fresh_ids)


def get_fresh_ids_itertools(fresh_ranges):
    ''' Also slow'''
    return list(set(chain.from_iterable(fresh_ranges)))


def get_fresh_ids_numpy(fresh_ranges):
    """Memory intesive but fast"""
    arrays = [np.arange(r.start, r.stop) for r in fresh_ranges]
    all_nums = np.concatenate(arrays)
    return np.unique(all_nums)


def get_fresh_ids_sort_and_merge(ranges):
    intervals = sorted((r.start, r.stop) for r in ranges)  # We need to sort first then merge any overlapping ranges.
    merged = []
    for start, stop in intervals:
        if not merged or merged[-1][1] < start:
            merged.append([start, stop])
        else:
            merged[-1][1] = max(merged[-1][1], stop)

    # Don't return all fresh produce ids since that takes way too much memory.
    #return [num for start, stop in merged for num in range(start, stop)]
    return sum(stop - start for start, stop in merged)  # We just care about the fresh produce count.


def main(args, data):
    #lines = [line for line in data.strip().split('\n') if line]
    lines = data.strip().split('\n')
    total = 0
    fresh_ranges = []
    for line in lines:
        if not line:
            continue
        if '-' in line:
            start, end = map(int, line.split('-'))
            fresh_ranges.append(range(start, end + 1))


    total = get_fresh_ids_sort_and_merge(fresh_ranges)

    assertions(args, total, 14, 367899984917516, 365804144481581)
    return total
    


if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    args = arg_parse(__file__, 'input2.txt', main)
    args = arg_parse(__file__, 'input3.txt', main)
