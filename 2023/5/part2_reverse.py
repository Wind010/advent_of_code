'''
--- Part Two ---

'''

from collections import defaultdict
import math
import re
from typing import List, Tuple
from common.common import arg_parse

from part1 import MAP_NAMES

from multiprocessing import Pool
from dataclasses import *
import time


@dataclass
class Range:
    start: int
    length: int
    end: int
    
    def __init__(self, start, length):
        self.start = start
        self.length = length
        self.end = start + length

    def contains(self, value: int) -> bool:
        return self.start <= value < self.end

    def overlaps(self, other: 'Range') -> bool:
        return not (self.end <= other.start or other.start + other.length <= self.start)

    def convert(self, src_start: int, dest_start: int) -> 'Range':
        diff = dest_start - src_start
        return Range(self.start + diff, self.length)
    

def check(loc: int) -> int | None:
    global seed_ranges
    global maps

    value = loc
    for m in maps:
        for dest_range, src_start in m:
            if dest_range.contains(value):
                value = src_start + (value - dest_range.start)
                break
    
    return loc if any(r.contains(value) for r in seed_ranges) else None


def parse_input(data: str) -> Tuple[List[Range], List[List[Tuple[Range, int]]]]:
    global seed_ranges
    global maps

    raw_seeds = list(map(int, data.split("\n")[0].split(": ")[1].split(" ")))
    seed_ranges = [Range(raw_seeds[i], raw_seeds[i + 1]) for i in range(0, len(raw_seeds), 2)]
    maps = []
    for sec in data.split("\n\n")[1:]:
        lines = sec.split("\n")
        m = []
        for line in lines[1:]:
            trg_start, src_start, length = map(int, line.split(" "))
            m.append((Range(trg_start, length), src_start))
        maps.append(m)

    return seed_ranges, maps

maps = []
seed_ranges = []

def main(file_path):
    global seed_ranges
    global maps
    data = open(file_path, 'r', encoding='utf-8').read()
    seed_ranges, maps = parse_input(data)
    maps = maps[::-1]

    start_time = time.time()
    min_location = math.inf
    with Pool(15) as pool:
        for loc in pool.imap(check, range(int(1e9)), int(1e6)):
            if loc is not None:
                min_location = min(loc, min_location)
                print(loc, min_location)
                print("Execution took {%s}", time.time()-start_time)
                return
            
        # for loc in pool.imap(worker, ((loc, seed_ranges, maps) for loc in range(int(1e9))), int(1e6)):
        #     if loc is not None:
        #         print(loc, min_location)
        #         print("Execution took {%s}", time.time()-start_time)
        #         return
            
    if 'input1.txt' in file_path: assert min_location == 46
    if 'input2.txt' in file_path: assert min_location == 2520479



if __name__ == "__main__":
    args = arg_parse(__file__, 'input1.txt', main)
    main(args.file_path)
    args = arg_parse(__file__, 'input2.txt', main)
    main(args.file_path)
